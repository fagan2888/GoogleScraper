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
import requests


# keywords = '/donald trump'

baseURL = 'https://www.google.com'
#imgURLS = ['/imgres?imgurl=http://static4.businessinsider.com/image/56c640526e97c625048b822a-480/donald-trump.jpg&imgrefurl=http://www.businessinsider.com/celebrities-who-support-trump-2016-10&h=360&w=480&tbnid=9goIX11Lf6XduM:&tbnh=150&tbnw=200&usg=__rLhTt6B-DGpWjBbUVZ3785y0jqo=&vet=1&docid=vpgNp0POhSJ00M&itg=1&sa=X&ved=0ahUKEwjMpLmQ7dnTAhVD8CYKHWfiBlIQ_B0IkgEwEw',
imgURLS = ['/search?q=donald+trump&biw=1200&bih=550&site=webhp&tbm=isch&imgil=Ug1Ps2oOonzUzM%253A%253Bx1JyCp6rSp5gbM%253Bhttps%25253A%25252F%25252Fgetreferralmd.com%25252F2016%25252F11%25252Fhow-trump-change-healthcare%25252F&source=iu&pf=m&fir=Ug1Ps2oOonzUzM%253A%252Cx1JyCp6rSp5gbM%252C_&usg=__eQ6QppUNtBmErKuNXpkEVNGzmyw%3D',
            '/search?q=donald+trump&biw=1200&bih=550&site=webhp&tbm=isch&imgil=mviNm0r25RO5hM%253A%253BI-S4cySxyxR1MM%253Bhttp%25253A%25252F%25252Ftheresurgent.com%25252Fchristians-for-trump-5-things-i-dont-understand%25252F&source=iu&pf=m&fir=mviNm0r25RO5hM%253A%252CI-S4cySxyxR1MM%252C_&usg=__GyYz35c4wjBDzTVbuIho4nmDLiI%3D',
            '/search?q=donald+trump&biw=1200&bih=550&site=webhp&tbm=isch&imgil=AvIrQaIpibwDJM%253A%253Bk2bramTA8sbvCM%253Bhttp%25253A%25252F%25252Fwww.businessinsider.com%25252Fdonald-trump-polls-leads-florida-michigan-ohio-2016-3&source=iu&pf=m&fir=AvIrQaIpibwDJM%253A%252Ck2bramTA8sbvCM%252C_&usg=__62wCLvCR78jo2zvgD2BPPz_Q-WQ%3D',
            '/search?q=donald+trump&biw=1200&bih=550&site=webhp&tbm=isch&imgil=yvFg3h-mcJTEHM%253A%253BBe0Hy908v_Nh6M%253Bhttp%25253A%25252F%25252Fwww.cnn.com%25252Fvideos%25252Fpolitics%25252F2016%25252F01%25252F18%25252Fdonald-trump-uk-parliament-petition-ban-foster-nr.cnn&source=iu&pf=m&fir=yvFg3h-mcJTEHM%253A%252CBe0Hy908v_Nh6M%252C_&usg=__m5EkeS7fNvRzhJsoOoxA1RSGCqA%3D',
            '/search?q=donald+trump&biw=1200&bih=550&site=webhp&tbm=isch&imgil=2gFInUg_uAVjpM%253A%253BRwPjzIoJ11z4mM%253Bhttps%25253A%25252F%25252Fsteemd.com%25252Frecent%25252Fdonald&source=iu&pf=m&fir=2gFInUg_uAVjpM%253A%252CRwPjzIoJ11z4mM%252C_&usg=__VHlG8lGJNjeWtgY4Ll88rWyLUOU%3D',
            '/search?q=donald+trump&biw=1200&bih=550&site=webhp&tbm=isch&imgil=jd-uVOAYRr-ELM%253A%253BoUQ97aEz8anNMM%253Bhttps%25253A%25252F%25252Fen.wikipedia.org%25252Fwiki%25252FDonald_Trump&source=iu&pf=m&fir=jd-uVOAYRr-ELM%253A%252CoUQ97aEz8anNMM%252C_&usg=__6JMJz73Vba0mdey6hEhQxeDlaCw%3D'
            ]

count = 0

while count < len(imgURLS):
    for url in imgURLS:
        imgURL = baseURL + url
        count += 1
        print("URL:  ", imgURL)

#candidate = serp.query.replace(' ', '_')
#imageFile = str(link.serp_id) + '_' + str(link.id) + '_' + candidate + '_' + str(link.rank) + '.jpg'
        imageFile = "phantomjs" + '_' + "Donald_Trump" + '_' + str(count) + '.jpg'

        driver = webdriver.PhantomJS('./phantomjs')
        driver.set_window_size(1020, 550)
        driver.wait = WebDriverWait(driver, 10)
        driver.get(imgURL)

        # element = driver.find_element_by_xpath('//*[@id="irc_cc"]/div[3]/div[1]/div[2]/div[2]/a/img')
        #element = driver.find_element_by_xpath('//*[@id="irc_cc"]/div[2]/div[1]/div[2]/div[2]/a/img')
        #element = driver.find_element_by_css_selector('#irc_cc > div:nth-child(2) > div.irc_t.i30052 > div.irc_mic.r-iUD5sHL57yas > div.irc_mimg.irc_hic.iUD5sHL57yas-lvVgf-rIiHk > a > img')
        try:
            #element = driver.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#irc_cc > div:nth-child(2) > div.irc_t > div.irc_mic > div.irc_mimg > a > img')))
            #element = driver.find_elements_by_css_selector('#irc_cc > div:nth-child(2) > div.irc_t > div.irc_mic > div.irc_mimg > a > img')
            #element = driver.find_element_by_xpath('//*[@id="irc_cc"]/div[2]/div[1]/div[2]/div[2]/a/img')           
            #element = driver.find_element_by_xpath('//*[@id="irc_mi"]')            
            #element = driver.find_element_by_id('#irc_mi') 
            #element = driver.wait.until(EC.presence_of_element_located((By.XPATH,'#irc_mi')))
            element = driver.wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="irc_cc"]/div[2]/div[1]/div[2]/div[2]/a/img')))

            src = element.get_attribute('src')
            print("SRC:   ", src)
   
            with open((imageFile), 'wb') as q:
                # get image from the link
                res = requests.get(src)

                # write the image to file in chunks
                for chunk in res.iter_content(100000):
                    q.write(chunk)
                    print("saved")
                
        except TimeoutException:
            print("oops timeout")

    
        
        driver.quit()
        time.sleep(5)
        
        count += 1

#//*[@id="irc_cc"]/div[2]/div[1]/div[2]/div[2]/a/img
# raw_page = driver.page_source
# b = BeautifulSoup(raw_page, 'lxml')
#
#
#
#
#
#
# def init_driver():
#     driver = webdriver.Firefox()
#     driver.wait = WebDriverWait(driver, 5)
#     return driver
#
# def get_image_url(driver, query):
#     driver.get(query)
#     print(query)
#     try:
#         box = driver.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,"irc_cc > div:nth-child(3) > div.irc_t > div.irc_mic.r-iJ8VSE_TmlGQ > div.irc_mimg.irc_hic.iJ8VSE_TmlGQ-lvVgf-rIiHk > a > img")))
#         image = box.getAttrubte("src")
#         print(image)
#     except TimeoutException:
#         print("Something like a timeout or something")
#
#     imageDriver.get(image)
#     try:
#         print("something")
#         #go to image url page and save jpg
#     except:
#         pass
#
#
# def lookup(driver, query):
#     driver.get("http://www.google.com")
#     try:
#         box = driver.wait.until(EC.presence_of_element_located(
#             (By.NAME, "q")))
#         button = driver.wait.until(EC.element_to_be_clickable(
#             (By.NAME, "btnK")))
#         box.send_keys(query)
#         button.click()
#     except TimeoutException:
#         print("Box or Button not found in google.com")
#
#
# if __name__ == "__main__":
#     driver = init_driver()
#     lookup(driver, "Selenium")
#     time.sleep(5)
#     driver.quit()
