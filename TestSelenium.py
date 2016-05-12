# -*- coding: utf-8 -*-
"""
Created on Sun May  1 23:56:08 2016

@author: jenniferstark
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import os
import requests


keywords = '/bernie sanders'

baseURL = 'https://www.google.com'
imgURLS = ["/imgres?imgurl=https://lh4.googleusercontent.com/-MoJHeOqT5Pg/AAAAAAAAAAI/AAAAAAAAUGY/QK9h6BxPcP8/s0-c-k-no-ns/photo.jpg&imgrefurl=http://plus.google.com/u/0/102227800261183349957&h=1382&w=1387&tbnid=RCn6RJLqg3Gu9M:&tbnh=186&tbnw=186&docid=iuPobGucMYk5mM&itg=1&usg=__Gw4GJBrdd45ni-r7TCNfQuq1mD4="]#,
           "/search?q=bernie+sanders&biw=400&bih=400&site=webhp&tbm=isch&imgil=IZe9q8twiLXe-M%253A%253B6hbbySYpkQ6H-M%253Bhttp%25253A%25252F%25252Fwww.huffingtonpost.com%25252Fseth-abramson%25252Fend-of-democratic-primary-means-anyone-who-ever-wanted-to-can-now-vote-for-bernie-sanders_b_9794770.html&source=iu&pf=m&fir=IZe9q8twiLXe-M%253A%252C6hbbySYpkQ6H-M%252C_&usg=__8FOpz2h671tVYoSyHOcSsP64cw8%3D",
           "/search?q=bernie+sanders&biw=400&bih=400&site=webhp&tbm=isch&imgil=HQCATCSeiTIx4M%253A%253B7lLiOY5RLQ2uNM%253Bhttp%25253A%25252F%25252Fwww.theonion.com%25252Fgraphic%25252Fwho-is-bernie-sanders-38525&source=iu&pf=m&fir=HQCATCSeiTIx4M%253A%252C7lLiOY5RLQ2uNM%252C_&usg=__OpzRqzaBbRwMTPLy5kdNARgpan0%3D",
           "/search?q=bernie+sanders&biw=400&bih=400&site=webhp&tbm=isch&imgil=nFEuuq8I17LLUM%253A%253BdhL4x_emiKzw3M%253Bhttp%25253A%25252F%25252Fwww.newyorker.com%25252Fnews%25252Fjohn-cassidy%25252Fbernie-sanders-loud-and-clear&source=iu&pf=m&fir=nFEuuq8I17LLUM%253A%252CdhL4x_emiKzw3M%252C_&usg=__i3jDwxJfqqTDnvJTY9NZyaQEV6U%3D",
           "/search?q=bernie+sanders&biw=400&bih=400&site=webhp&tbm=isch&imgil=b3DN2-_xskv-EM%253A%253BvjH1NMiagPkCZM%253Bhttp%25253A%25252F%25252Fwww.biography.com%25252Fpeople%25252Fbernie-sanders&source=iu&pf=m&fir=b3DN2-_xskv-EM%253A%252CvjH1NMiagPkCZM%252C_&usg=__XH5TPh9qpblxxu3tJ2UvMViF6u4%3D"]
          
count = 0

while count < len(imgURLS):
    for url in imgURLS:
        imgURL = baseURL + url
        print(imgURL)
    
#candidate = serp.query.replace(' ', '_')
#imageFile = str(link.serp_id) + '_' + str(link.id) + '_' + candidate + '_' + str(link.rank) + '.jpg'
        imageFile = "phantomjs" + '_' + "23" + '_' + "bernie_sanders" + '_' + str(count) + '.jpg'

        driver = webdriver.PhantomJS('./phantomjs')
        driver.wait = WebDriverWait(driver, 5)
        driver.get(imgURL)

        element = driver.find_element_by_xpath('//*[@id="irc_cc"]/div[3]/div[1]/div[2]/div[2]/a/img')
        src = element.get_attribute('src')

        with open((imageFile), 'wb') as q:
            # get image from the link
            res = requests.get(src)
                                        
            # write the image to file in chunks
            for chunk in res.iter_content(100000):
                q.write(chunk)
                print("saved")
    
    count += 1





raw_page = driver.page_source
b = BeautifulSoup(raw_page, 'lxml')






def init_driver():
    driver = webdriver.Firefox()
    driver.wait = WebDriverWait(driver, 5)
    return driver
 
def get_image_url(driver, query):
    driver.get(query)
    print(query)
    try:
        box = driver.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,"irc_cc > div:nth-child(3) > div.irc_t > div.irc_mic.r-iJ8VSE_TmlGQ > div.irc_mimg.irc_hic.iJ8VSE_TmlGQ-lvVgf-rIiHk > a > img")))
        image = box.getAttrubte("src")   
        print(image)
    except TimeoutException:
        print("Something like a timeout or something")
    
    imageDriver.get(image)
    try:
        print("something")
        #go to image url page and save jpg
    except:
        pass
    
        
def lookup(driver, query):
    driver.get("http://www.google.com")
    try:
        box = driver.wait.until(EC.presence_of_element_located(
            (By.NAME, "q")))
        button = driver.wait.until(EC.element_to_be_clickable(
            (By.NAME, "btnK")))
        box.send_keys(query)
        button.click()
    except TimeoutException:
        print("Box or Button not found in google.com")
 
 
if __name__ == "__main__":
    driver = init_driver()
    lookup(driver, "Selenium")
    time.sleep(5)
    driver.quit()