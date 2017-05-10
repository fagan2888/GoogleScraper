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
import configparser

# import scheduler things
from apscheduler.schedulers.background import BackgroundScheduler
import time

# Load KEYS.config file
config = configparser.ConfigParser()
config.read("keys.conf")

# AWS Database information
aws_username = config.get("AWSDatabaseConfig", "username")
aws_password = config.get("AWSDatabaseConfig", "password")
aws_host = config.get("AWSDatabaseConfig", "host")

###############################################################################

# Insert keywords to search as a list of strings
keywords = [
    'marine le pen',
    'angela merkel',
    'emmanuel macron',
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
    'log_level': 'INFO',  # change to DEBUG if you need more info
    'search_type': 'normal',
    'clean_cache_files': False,
    'print_results': 'summarize',

}

# Start the counter on 23 if you want to collect images on the first scrape.
# Code currently set to scrape once per hour and only colllect images once per day.
counter = 23

def put_in_database():

    # This block removes the database created in the previous scrape. It was easier to do this
    # than to remove the database code from this software.
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

    # Connect to database
    db = pymysql.connect(user= aws_username,  # Username of AWS database
                                 passwd= aws_password,  # AWS Database password
                                 host= aws_host,  # AWS Instance
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

            serp_id = cur.lastrowid
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

                    # IMAGE SAVE LOOP
                    if counter % 24 == 0:
                        print("\nStarting image save loop...:   ")
                        baseURL = 'https://www.google.com'
                        #print("Creating imgURL ...   ")

                        # This `imgURL` link should take you to the Google Image Search result with the image in question "selected" or expanded
                        imgURL = baseURL + link.link
                        print("Creating 'candidate' ...   \n", imgURL)

                        # Create image output file name
                        candidate = serp.query.replace(' ', '_')
                        print(candidate)
                        print("Creating candidate file name ....   ")
                        imageFile = str(serp_id) + '_' + str(link.id) + '_' + candidate + '_' + str(link.rank) + '.jpg'
                        print(imageFile)

                        # Initilize phantomjs headless browser
                        #http://www.marinamele.com/selenium-tutorial-web-scraping-with-selenium-and-python
                        #http://stackoverflow.com/questions/15388057/extract-link-from-xpath-using-selenium-webdriver-and-python
                        dcap = dict(DesiredCapabilities.PHANTOMJS)
                        dcap["phantomjs.page.settings.userAgent"] = random_user_agent(only_desktop=True)

                        driver = webdriver.PhantomJS('./phantomjs', desired_capabilities=dcap)
                        driver.set_window_size(1020, 550)
                        driver.wait = WebDriverWait(driver, 5)

                        # Use the try statement if to continue to collect images even when a collection fails.
                        # If you want scraping to quit when image collection fails, take out the try statement. 
                        try:
                            driver.get(imgURL)

                            # CURENT_XPATH freqently changes, so keep an eye on this. If your images suddenly fail to download, this is where to check first.
                            element = driver.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="irc_cc"]/div[2]/div[1]/div[2]/div[2]/a/img'))) # this is the current one.
                            time.sleep(4) #4
                            src = element.get_attribute('src')
                            print("This is the 'src':   ", src)
                            time.sleep(4) #4

                            # Create direcory named using the current serp_id
                            # There will be one serp_id per keyword search
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

                        except Exception as e:
                            # Recently image collection has been buggy inconsistenly.
                            # If image download fails, this exception will take a
                            # screenshot and save to the main directory.
                            driver.save_screenshot(imageFile + '.png')
                            pass

                        driver.close()
                        driver.quit()


                    else: image_path = None

                else:
                    image_height = None
                    image_width = None
                    image_path = None


                # Create a new record into search_engine_results table
                sql = "INSERT INTO search_engine_results (link, title, snippet, visible_link, rank, link_type, serp_id, has_image, image_dims, image_height, image_width, news_date, news_source, image_path, top_stories) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                cur.execute(sql,(link.link, link.title, link.snippet, link.visible_link, link.rank, link.link_type, serp_id, link.has_image, link.image_dims, image_height, image_width, link.news_date, link.news_source, image_path, link.top_stories))

                db.commit()

    finally:
        cur.close()
        db.close()

# # Create a scheduler to trigger every N seconds
# # http://apscheduler.readthedocs.org/en/3.0/userguide.html#code-examples
scheduler = BackgroundScheduler()
# for testing, use shorter interval (eg 300 seconds or 60 seconds...)
# Can change interval to minutes or hours if more appropriate
scheduler.add_job(put_in_database, 'interval', seconds = 3600) #  3600 = 1 hour
scheduler.start()

while True:
	time.sleep(1)


# nohup python -u candidate_scraper.py > nohup.txt &
