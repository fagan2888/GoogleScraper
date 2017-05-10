# -*- coding: utf-8 -*-
"""
Created on Wed Jun 15 21:31:13 2016

@author: jenniferstark
"""

# Our own DB things
import pymysql
import pymysql.cursors

import datetime
import sys

# url requests...
import time
import requests

# timer set to run every 60 minutes
from apscheduler.schedulers.background import BackgroundScheduler



def text_stats():
# 3000 API calls per day = 125 calls per hour
# alchemy key and api endpoints:
    apikey = '116253b1d06454f4eb18086999a9a375a371ece3' # ND key
    #apikey = "3f9bbc00f9a0e6c2cc8adea331e76592b53a5464" # my temp key
    urlsentiment_api = 'http://gateway-a.watsonplatform.net/calls/url/URLGetTextSentiment' # sentiment analysis of url content


    db = pymysql.connect(user='merrillawsdb',
                             passwd='WR3QZGVaoHqNXAF',
                             host='awsdbinstance.cz5m3w6kwml8.us-east-1.rds.amazonaws.com',
                             port=3306,
                             database='google_scraper',
                             charset='utf8mb4')

    cursor = db.cursor(pymysql.cursors.DictCursor)

    # fetch up to 1000 rows from the DB that are 'results' pages, and have not yet been analyzed
    sql = "SELECT * from search_engine_results_TESTING WHERE link_type = 'results' AND content_HTML is NULL LIMIT 500"
    cursor.execute(sql)

    results = cursor.fetchall()

    try:
        print("starting loop now")
        for row in results:
            print(row['id'])

            content_HTML = None
            content_text = None
            doc_sentiment = None
            doc_score = None
            doc_mixed = None
            grab_datetime = None


            # Getting raw html string data:
            try:
                print('Getting request for content_HTML')
                r = requests.get(row['link'])
                # Avoid to put into variable if size HTML code is too big
                if sys.getsizeof(r.text) < 4098871:
                    content_HTML = r.text
                    r.close()
            except Exception as e:
                print('requests error for content_HTML')
                print (e)
                print (row(['link']))

            time.sleep(3)

            # Document sentiment analysis + get cleaned text (showSourceText)
            try:
                print('Getting request for alchemy')
                r = requests.get(urlsentiment_api, params={'apikey': apikey, 'url': row['link'], 'outputMode': 'json', 'showSourceText':1})
                #print(r)
                doc_response = r.json()
                #print(doc_response)

                if doc_response['status'] == 'OK':
                    doc_sentiment = doc_response['docSentiment']['type']
                    content_text = doc_response['text']
                    if 'score' in doc_response['docSentiment']:
                        doc_score = doc_response['docSentiment']['score']
                    if 'mixed' in doc_response['docSentiment']:
                        doc_mixed = doc_response['docSentiment']['mixed']
                else:
                    print ( 'Error in sentiment analysis call: ', doc_response['statusInfo'])

            except Exception as e:
                print('requests error for Alchemy')
                print(e)


            grab_datetime = datetime.datetime.now()
            print('grab_datetime', grab_datetime)


            query = "UPDATE search_engine_results_TESTING SET content_HTML = %s, content_text = %s, doc_sentiment = %s, doc_score = %s, doc_mixed = %s, grab_datetime = %s WHERE id = %s"
            data = (content_HTML, content_text, doc_sentiment, doc_score, doc_mixed, grab_datetime, row['id'])

            cursor.execute(query, data)

            db.commit()

    finally:
        cursor.close()
        db.close()


# # Taken from Uber gatherUberData.py
# # Create a scheduler to trigger every N seconds
# # http://apscheduler.readthedocs.org/en/3.0/userguide.html#code-examples
scheduler = BackgroundScheduler()
scheduler.add_job(text_stats, 'interval', minutes = 60)
scheduler.start()

while True:
	time.sleep(1)


# nohup python -u text_analysis.py > nohup_text_analysis.txt &
