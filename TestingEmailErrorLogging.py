# -*- coding: utf-8 -*-
"""
Created on Tue May 10 17:24:23 2016

@author: jenniferstark
"""

import logging
import logging.handlers

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
import time

#from io import StringIO

import smtplib
from email.mime.text import MIMEText

HOST = 'localhost'
FROM = '"Application Alert" <cjl.at.umd@gmail.com>'
TO = 'jastark1@gmail.com'
SUBJECT = 'GoogleScraper Error'

smtp_handler = logging.handlers.SMTPHandler(#mailhost=("aspmx.l.google.com", 25),
                                            #mailhost=('smtp.gmail.com'),
                                            mailhost=('smtp-relay.gmail.com', 25),
                                            #credentials=('cjl.at.umd','C0mpJ0urn'),
                                            credentials=('192.168.1.134'),
                                            fromaddr="cjl.at.umd@gmail.com",
                                            toaddrs=["jastark1@gmail.com"],
                                            subject="GoogleScraper XPATH error!")


smtp_handler = logging.handlers.SMTPHandler(HOST, FROM, TO, SUBJECT)

logger = logging.getLogger()
logger.addHandler(smtp_handler)

baseURL = 'https://www.google.com'

imgURL = baseURL + '/search?q=donald+trump&biw=1200&bih=1200&site=webhp&tbm=isch&imgil=9BmBzOYbU5_BUM%253A%253Bu6mdGIvmKrKG5M%253Bhttp%25253A%25252F%25252Fwww.theonion.com%25252Ftag%25252Fdonald-trump&source=iu&pf=m&fir=9BmBzOYbU5_BUM%253A%252Cu6mdGIvmKrKG5M%252C_&usg=__g5EpMg_yG8N_3tetQ5CwRrlUOfg%3D'


dcap = dict(DesiredCapabilities.PHANTOMJS)
dcap["phantomjs.page.settings.userAgent"] = random_user_agent(only_desktop=True)

driver = webdriver.PhantomJS('./phantomjs', desired_capabilities=dcap)
driver.set_window_size(1020, 550)
driver.wait = WebDriverWait(driver, 5)
driver.get(imgURL)
#element = driver.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="irc_cc"]/div[2]/div[1]/div[2]/div[2]/a/img'))) # this is the current one.
element = driver.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="irc_cc"]/div[1]/div[1]/div[2]/div[2]/a/img'))) # this is the old one.
time.sleep(4)
src = element.get_attribute('src')
print("This is the 'src':   ", src)
time.sleep(4)

me = 'cjl.at.umd@gmail.com'
you = 'jastark1@gmail.com'
message = 'something wrong with GoogleScraper. Check out the nohup.txt file'

imageFile = 'TestingmailErrorLogging.png'
try:
    with open((imageFile), 'wb') as q:
        # get image from the link
        res = requests.get(src)
        # write the image to file in chunks
        for chunk in res.iter_content(100000):
            q.write(chunk)
except Exception as e:
    logger.exception('Unhandled Exception')
    #msg = MIMEText(message)
    #fp.close()
    
    #msg['Subject'] = "GoogleScraper Error"
    #msg['From'] = me
    #msg['To'] = you
    
    #s = smtplib.SMTP('localhost')
    #s.sendmail(me, [you], msg.as_string())
    #s.quit()
    #print("Error - file not created")
    


driver.close()
driver.quit()



try: 
    with open('TestingmailErrorLogging.png','r') as f:
        output = f.read()
        print("File opened")
except Exception as e:
    logger.exception('Unhandled Exception')
    print("Error - file not opened")
    
    



import logging
from logging import handlers
import socket
import traceback

HOST = 'aspmx.l.google.com'
FROM = 'cjl.at.umd@gmail.com'
TO = 'jastark1@gmail.com'
SUBJECT = 'New Critical Event From [APPLICATION]'
CREDENTIALS = ('cjl.at.umd','C0mpJ0urn')

# Setup logging
logging.basicConfig(level=logging.INFO)

handler = handlers.SMTPHandler(HOST, FROM, TO, SUBJECT)
email_logger = logging.getLogger('smtp.example')
email_logger.addHandler(handler)
email_logger.setLevel = logging.CRITICAL

logging.info('Root logger output')
try:
    email_logger.critical('Critical Event Notification\n\nTraceback:\n %s',
                          ''.join(traceback.format_stack()))
except socket.error as error:
    logging.critical('Could not send email via SMTPHandler: %r', error)







# http://stackoverflow.com/questions/8616617/how-to-make-smtphandler-not-block

import logging.handlers
import smtplib
from threading import Thread

def smtp_at_your_own_leasure(mailhost, port, username, password, fromaddr, toaddrs, msg):
    smtp = smtplib.SMTP(mailhost, port)
    if username:
        smtp.ehlo() # for tls add this line
        smtp.starttls() # for tls add this line
        smtp.ehlo() # for tls add this line
        smtp.login(username, password)
    smtp.sendmail(fromaddr, toaddrs, msg)
    smtp.quit()

class ThreadedTlsSMTPHandler(logging.handlers.SMTPHandler):
    def emit(self, record):
        try:
            import string # for tls add this line
            try:
                from email.utils import formatdate
            except ImportError:
                formatdate = self.date_time
            port = self.mailport
            if not port:
                port = smtplib.SMTP_PORT
            msg = self.format(record)
            msg = "From: %s\r\nTo: %s\r\nSubject: %s\r\nDate: %s\r\n\r\n%s" % (
                            self.fromaddr,
                            string.join(self.toaddrs, ","),
                            self.getSubject(record),
                            formatdate(), msg)
            thread = Thread(target=smtp_at_your_own_leasure, args=(self.mailhost, port, self.username, self.password, self.fromaddr, self.toaddrs, msg))
            thread.start()
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)




logger = logging.getLogger()

gm = ThreadedTlsSMTPHandler(("smtp.gmail.com", 587), 'bugs@my_company.com', ['admin@my_company.com'], 'Error found!', ('my_company_account@gmail.com', 'top_secret_gmail_password'))
gm.setLevel(logging.ERROR)

logger.addHandler(gm)

try:
    1/0
except:
    logger.exception('FFFFFFFFFFFFFFFFFFFFFFFUUUUUUUUUUUUUUUUUUUUUU-')
    
    