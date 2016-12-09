#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
based on `./Examples/http_mode_example.py`
'''
# scraper things
from GoogleScraper import scrape_with_config, GoogleSearchError

# Our own DB things
import pymysql
import pymysql.cursors

#from selenium import webdriver for phantomjs image download
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from GoogleScraper.user_agents import random_user_agent

# import  stuff for image download and file manipulation
import os
import requests
import re

# import scheduler things
from apscheduler.schedulers.background import BackgroundScheduler
import time


counter = 23

keywords = [
    'bernie sanders',
    'hillary clinton',
    'donald trump'
]

# See in the config.cfg file for possible values
config = {
    'use_own_ip': True,
    'keywords': keywords,
    'search_engines': ['google',],
    'num_pages_for_keyword': 1,
    'scrape_method': 'selenium',
    'do_caching': False,
    'sel_browser': 'phantomjs',
    'log_level': 'INFO',
    'search_type': 'normal',
    'clean_cache_files': False,
    'print_results': 'summarize',

}


def put_in_database():


    try:
        os.remove("google_scraper.db")
        print("\nSQLite database Removed!")
    except:
        print("\nNo database to remove")


    global counter
    counter += 1
    print("The current count is: ", counter)


    try:
        search = scrape_with_config(config)
    except GoogleSearchError as e:
        print(e)


    db = pymysql.connect(user='merrillawsdb',
                                 passwd='WR3QZGVaoHqNXAF',
                                 host='awsdbinstance.cz5m3w6kwml8.us-east-1.rds.amazonaws.com',
                                 port=3306,
                                 database='google_scraper',
                                 charset='utf8mb4')
    cur = db.cursor()


    target_directory = './images/'
    try:
        os.mkdir(target_directory)
    except FileExistsError:
        pass


    try:
        for serp in search.serps:

            # Create a new record into serp table
            sql = "INSERT INTO serp (search_engine_name, scrape_method, requested_at, search_query) VALUES (%s, %s, %s, %s)"
            cur.execute(sql,(serp.search_engine_name, serp.scrape_method, serp.requested_at, serp.query))

            serp_id = cur.lastrowid  # This line can go before or after db.commit()
            print("\nserp_id is:  ", serp_id)

            db.commit()


            for link in serp.links:

                if link.has_image:
                    link.has_image = 1
                else: link.has_image = 0

                if link.link_type == 'image_box':

                    height = re.compile('height:(\d+)')
                    h = height.search(link.image_dims)
                    image_height = int(h.group(1))

                    width = re.compile('width:(\d+)')
                    w = width.search(link.image_dims)
                    image_width = int(w.group(1))

                    if counter % 24 == 0:
                        print("\nStarting image save if-loop...:   ")
                        baseURL = 'https://www.google.com'
                        #print("Creating imgURL ...   ")
                        imgURL = baseURL + link.link
                        #print("Creating 'candidate' ...   \n", imgURL)
                        candidate = serp.query.replace(' ', '_')
                        print(candidate)
                        print("Creating candidate file name ....   ")
                        imageFile = str(serp_id) + '_' + str(link.id) + '_' + candidate + '_' + str(link.rank) + '.jpg'
                        print(imageFile)

                        #http://www.marinamele.com/selenium-tutorial-web-scraping-with-selenium-and-python
                        #http://stackoverflow.com/questions/15388057/extract-link-from-xpath-using-selenium-webdriver-and-python
                        dcap = dict(DesiredCapabilities.PHANTOMJS)
                        dcap["phantomjs.page.settings.userAgent"] = random_user_agent(only_desktop=True)

                        driver = webdriver.PhantomJS('./phantomjs', desired_capabilities=dcap)
                        driver.set_window_size(1020, 550)
                        driver.wait = WebDriverWait(driver, 5)
                        driver.get(imgURL)

                        element = driver.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="irc_cc"]/div[2]/div[1]/div[2]/div[2]/a/img'))) # this is the current one.
                        #element = driver.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="irc_cc"]/div[3]/div[1]/div[2]/div[2]/a/img'))) # this is the old one.
                        time.sleep(4)
                        src = element.get_attribute('src')
                        print("This is the 'src':   ", src)
                        time.sleep(4)

                        current_directory = str(serp_id) + '/'
                        path = os.path.join(target_directory, current_directory)
                        if not os.path.exists(path):
                            os.makedirs(path)

                        image_path = path + imageFile

                        with open(os.path.join(path,imageFile), 'wb') as q:
                            # get image from the link
                            res = requests.get(src)
                            # write the image to file in chunks
                            for chunk in res.iter_content(100000):
                                q.write(chunk)

                        driver.close()
                        driver.quit()


                    else: image_path = None

                else:
                    image_height = None
                    image_width = None
                    image_path = None


                # Create a new record into search_engine_results table
                sql = "INSERT INTO search_engine_results (link, title, snippet, visible_link, rank, link_type, serp_id, has_image, image_dims, image_height, image_width, news_date, news_source, image_path) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                cur.execute(sql,(link.link, link.title, link.snippet, link.visible_link, link.rank, link.link_type, serp_id, link.has_image, link.image_dims, image_height, image_width, link.news_date, link.news_source, image_path))

                db.commit()

    finally:
        cur.close()
        db.close()

# # Taken from Uber gatherUberData.py
# # Create a scheduler to trigger every N seconds
# # http://apscheduler.readthedocs.org/en/3.0/userguide.html#code-examples
scheduler = BackgroundScheduler()
scheduler.add_job(put_in_database, 'interval', seconds =3600) # 1 hour
scheduler.start()

while True:
	time.sleep(1)


# nohup python -u candidate_scraper.py > nohup.txt &
