#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
This is an example script for testing data-gathering time intervals.
Perhaps the thing you're collecting changes every N moments. What is the optimal
time interval for collection to ensure you don't miss anything?

This example looks at the "Top Stories" on the Google main search results
page.

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
import datetime

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
    'vladimir putin',
    # 'nba',
    # 'donald trump'
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
    'log_level': 'INFO',  #use DEGUB for more
    'search_type': 'normal',
    'clean_cache_files': False,
    'print_results': 'summarize',

}

# How many times you want to collect each time interval
repeat_num = 3
counter = 0

# The timer intervals, currently in seconds
timer_interval = [120, 200, 300]

# This is the interval the first set of repeats will run on. This number should
# not be included in the timer_interval list.
current_interval = 60

def put_in_database():


    try:
        os.remove("google_scraper.db")
        print("\nSQLite database Removed!")
    except:
        print("\nNo database to remove")


    global counter, scheduler, timer_interval, current_interval

    counter += 1
    print("The current count is: ", counter)
    scheduler.print_jobs()


    try:
        search = scrape_with_config(config)
    except GoogleSearchError as e:
        print(e)


    db = pymysql.connect(user= aws_username,  # Username of AWS database
                                 passwd= aws_password,  # AWS Database password
                                 host= aws_host,  # AWS Instance
                                 port=3306,
                                 database='google_scraper',
                                 charset='utf8mb4')
    cur = db.cursor()


    try:
        for serp in search.serps:

            # Create a new record into serp table
            sql = "INSERT INTO serp_topstories_TESTING (search_engine_name, scrape_method, requested_at, search_query) VALUES (%s, %s, %s, %s)"
            cur.execute(sql,(serp.search_engine_name, serp.scrape_method, serp.requested_at, serp.query))

            serp_id = cur.lastrowid  # This line can go before or after db.commit()
            print("\nserp_id is:  ", serp_id)

            db.commit()


            for link in serp.links:

                if link.link_type == "top_stories":

                    if link.has_image:
                        link.has_image = 1
                    else: link.has_image = 0

                    print("\nCurrent Interval is:  ", current_interval)
                    get_datetime = datetime.datetime.now()
                    print(datetime.datetime.now())
                    # Create a new record into search_engine_results table
                    sql = "INSERT INTO search_engine_topstories_TESTING (link, title, rank, link_type, serp_id, has_image, image_dims, news_date, news_source, timer_interval, get_datetime) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                    cur.execute(sql,(link.link, link.title, link.rank, link.link_type, serp_id, link.has_image, link.image_dims, link.news_date, link.news_source, current_interval, get_datetime))

                    db.commit()

    finally:
        cur.close()
        db.close()


    if counter == repeat_num:

        # enter this section once completed desired number of repetitions as denoted by repeat_num
        # if there are remaining intervals left, do:
        if timer_interval:

            counter = 0

            print("\nThe next interval time is: ", timer_interval[0])
            current_interval = timer_interval[0]
            scheduler.reschedule_job('job_1', trigger='interval', seconds=timer_interval[0])
            timer_interval.pop(0)

        # if there are no more intervals left, we're done:
        else:
            print("\nList is now empty. Finished Loops")
            scheduler.shutdown(wait=False)




if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    scheduler.add_job(put_in_database, 'interval', seconds=current_interval, id='job_1', replace_existing=True)
    scheduler.start()

    try:
        # This is here to simulate application activity (which keeps the main thread alive).
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        # Not strictly necessary if daemonic mode is enabled but should be done if possible
        scheduler.shutdown()

# nohup python -u top_stories_time_testing.py > nohup_intervals.txt &
