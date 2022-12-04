import os

from django.shortcuts import render ,redirect

import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from .models import *
from django.contrib import messages
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def scraper(request):
     fb_credentails = Fb_credentails.objects.get(owner=request.user)

    #  option = Options()
    #  # Working with the 'add_argument' Method to modify Driver Default Notification
    #  option.add_argument('--disable-notifications')
    # #  Passing Driver path alongside with Driver modified Options
    #  driver = webdriver.Chrome(executable_path=  r"Scraper/chromedriver.exe", chrome_options= option)

    #  driver.get("https://www.facebook.com/login.php/")
     #  #here is code for heroku web drivers

     url = 'https://www.facebook.com/login.php/'

     options = webdriver.ChromeOptions()

     options.add_experimental_option("detach", True)
     options.add_experimental_option(
         'excludeSwitches', ['enable-logging'])  # for skipping the warning
     options.headless = True

     chrome_options = webdriver.ChromeOptions()
     chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
     chrome_options.add_argument("--headless")
     chrome_options.add_argument("--disable-dev-shm-usage")
     chrome_options.add_argument("--no-sandbox")
     chrome_options.add_argument("--disable-notifications")
     driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
     driver.get(url)

     print('Line no 52 Login done successfully.')














     inputElementEmail = driver.find_element("css selector", "input[type='text']")
     inputElementEmail.send_keys(fb_credentails.username)    
     time.sleep(10)
     inputElementPassword = driver.find_element("css selector", "input[type='password']")
     inputElementPassword.send_keys(fb_credentails.password)
     loginbutton=driver.find_element("xpath",'//*[@id="loginbutton"]')
     loginbutton.click()
     time.sleep(5)
     driver.get("https://www.facebook.com/marketplace/create/item")


     time.sleep(10)


     products_data = Product.objects.filter(owner=request.user)
     for products in products_data:
        title = driver.find_element("xpath","//span[text()='Title']//following-sibling::input")
        title.send_keys(products.title)

        price = driver.find_element("xpath","//span[text()='Price']//following-sibling::input")
        price.send_keys(products.price)

        desc = driver.find_element("xpath","//span[text()='Description']//following-sibling::textarea")
        desc.send_keys(products.desc)

        condition_btn_dropdown=driver.find_element("xpath","//span[text()='Condition']//following-sibling::div")
        condition_btn_dropdown.click()
        time.sleep(2)
        condition_btn_dropdown=driver.find_element("xpath","//span[text()='New']")
        condition_btn_dropdown.click()
        time.sleep(2)
        category_btn=driver.find_element("xpath","//span[text()='Category']//following-sibling::div")
        category_btn.click()

        category_btn_dropdown=driver.find_element("xpath","//span[text()='Furniture']")
        category_btn_dropdown.click()
        time.sleep(2)
        driver.find_element("xpath","//span[text()='Location']//following-sibling::input").send_keys(Keys.CONTROL + "a")
        driver.find_element("xpath","//span[text()='Location']//following-sibling::input").send_keys(Keys.DELETE)
        time.sleep(2)
        location = driver.find_element("xpath","//span[text()='Location']//following-sibling::input")
        location.send_keys(products.location)
        time.sleep(3)
        location.send_keys(Keys.ARROW_DOWN)
        location.send_keys(Keys.RETURN)
        time.sleep(2)
        file_upload= driver.find_element("xpath","//input[@type='file']")
        file_upload.send_keys(products.image.path)
        time.sleep(5)
        try:
            tag1 = driver.find_element("xpath","//textarea[@id='jsc_c_1a']")
        except:
            tag1 = driver.find_element("xpath","//textarea[@id='jsc_c_1b']")
        tag1.send_keys(products.tag1)
        tag1.send_keys(Keys.RETURN)
        time.sleep(3)
        try:
            tag2 = driver.find_element("xpath","//textarea[@id='jsc_c_1a']")
        except:
            tag2 = driver.find_element("xpath","//textarea[@id='jsc_c_1b']")
        tag2.send_keys(products.tag2)
        tag2.send_keys(Keys.RETURN)
        time.sleep(3)
        try:
            tag3 = driver.find_element("xpath","//textarea[@id='jsc_c_1a']")
        except:
            tag3 = driver.find_element("xpath","//textarea[@id='jsc_c_1b']")
        tag3.send_keys(products.tag3)
        tag3.send_keys(Keys.RETURN)
        time.sleep(3)
        try:
            tag4 = driver.find_element("xpath","//textarea[@id='jsc_c_1a']")
        except:
            tag4 = driver.find_element("xpath","//textarea[@id='jsc_c_1b']")
        tag4.send_keys(products.tag4)
        tag4.send_keys(Keys.RETURN)
        time.sleep(3)
        try:
            tag5 = driver.find_element("xpath","//textarea[@id='jsc_c_1a']")
        except:
            tag5 = driver.find_element("xpath","//textarea[@id='jsc_c_1b']")
        tag5.send_keys(products.tag5)
        tag5.send_keys(Keys.RETURN)
        time.sleep(3)

        time.sleep(3)
        next_btn=driver.find_element("xpath","//span[text()='Next']")
        next_btn.click()
        time.sleep(5)
        publish_btn=driver.find_element("xpath","//span[text()='Publish']")
        publish_btn.click()
        products.status="published"
        products.save()
        driver.get("https://www.facebook.com/marketplace/create/item")
        time.sleep(10)
     messages.success(request, 'Ads uploaded successfully')
     return redirect('dashboard')
     #

