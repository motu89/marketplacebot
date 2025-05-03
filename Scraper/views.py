from django.shortcuts import render ,redirect, get_object_or_404
from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from .models import *
from django.contrib import messages

def scraper(request):
     fb_credentails = Fb_credentails.objects.filter(owner=request.user)
     for fb_credentail in fb_credentails:
        # Use the first Facebook account by default
        publish_with_fb_account(request, fb_credentail)
     messages.success(request, 'Ads uploaded successfully')
     return redirect('dashboard')

def scraper_with_account(request, account_number):
    try:
        fb_account = Fb_credentails.objects.get(owner=request.user, account_number=account_number)
        publish_with_fb_account(request, fb_account)
        messages.success(request, f'Ads uploaded successfully using {fb_account.account_name or f"Account #{account_number}"}')
    except Fb_credentails.DoesNotExist:
        messages.error(request, f'Facebook account #{account_number} not found. Please set it up first.')
    except Exception as e:
        # Catch any other errors that might occur during publishing
        messages.error(request, f'Error publishing ads: {str(e)}')
    
    return redirect('facebook_accounts')  # Redirect back to Facebook accounts page

def publish_with_fb_account(request, fb_account):
    option = Options()
    # Working with the 'add_argument' Method to modify Driver Default Notification
    option.add_argument('--disable-notifications')
    #  Passing Driver path alongside with Driver modified Options
    driver = webdriver.Chrome(executable_path=  r"Scraper/chromedriver.exe", chrome_options= option)
    driver.get("https://www.facebook.com/login.php/")

    inputElementEmail = driver.find_element("css selector", "input[type='text']")
    inputElementEmail.send_keys(fb_account.username)    
    time.sleep(10)
    inputElementPassword = driver.find_element("css selector", "input[type='password']")
    inputElementPassword.send_keys(fb_account.password)
    loginbutton=driver.find_element("xpath",'//*[@id="loginbutton"]')
    loginbutton.click()
    time.sleep(60)
    driver.get("https://www.facebook.com/marketplace/create/item")
    time.sleep(10)
    products_data = Product.objects.filter(owner=request.user)
    for products in products_data:
        title = driver.find_element("xpath","//span[text()='Title']//following-sibling::input")
        title.send_keys(products.title)
        time.sleep(5)
        price = driver.find_element("xpath","//span[text()='Price']//following-sibling::input")
        price.send_keys(products.price)
        
        time.sleep(5)
        condition_btn_dropdown=driver.find_element("xpath","//span[text()='Condition']//following-sibling::div")
        condition_btn_dropdown.click()
        time.sleep(2)
        try:
            condition_btn_dropdown=driver.find_element("xpath","//span[text()='New']")
            condition_btn_dropdown.click()
        except:
            try:
                condition_btn_dropdown1=driver.find_element("xpath","/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[2]/div/div/div[1]/div[1]/div/div/div/div/div[1]/div/div[1]")
                condition_btn_dropdown1.click()
            except:
                condition_btn_dropdown=driver.find_element("xpath","/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div[1]/div/div[3]/div[1]/div[2]/div/div/div[8]/div/div/div/label/div/div[1]/div/div/span")
                condition_btn_dropdown.click()
        time.sleep(3)
        category_btn=driver.find_element("xpath","//span[text()='Category']//following-sibling::div")
        category_btn.click()
        time.sleep(3)
        category_btn_dropdown=driver.find_element("xpath","//span[text()='Furniture']")
        category_btn_dropdown.click()
        time.sleep(2)
        desc =  driver.find_element(By.XPATH, "//textarea[starts-with(@id, '«r')]")
        desc.send_keys(products.desc)
        time.sleep(2)
        driver.find_element("xpath","//span[text()='Location']//following-sibling::input").send_keys(Keys.CONTROL + "a")
        driver.find_element("xpath","//span[text()='Location']//following-sibling::input").send_keys(Keys.DELETE)
        time.sleep(2)
        location = driver.find_element("xpath","//span[text()='Location']//following-sibling::input")
        location.send_keys(products.location)
        time.sleep(3)
        location.send_keys(Keys.ARROW_DOWN)
        time.sleep(3)
        location.send_keys(Keys.RETURN)
        time.sleep(2)
        file_upload= driver.find_element("xpath","//input[@type='file']")
        file_upload.send_keys(products.image.path)
        time.sleep(5)
        try:
            tag1 = driver.find_element(By.XPATH, "(//textarea[starts-with(@id, '«r')])[2]")
        except:
            try:
                tag1 = driver.find_element("xpath","//textarea[@id='jsc_c_1b']")
            except:
                try:
                    tag1 = driver.find_element("xpath","//textarea[@id='jsc_c_26']")
                except:
                    try:
                        tag1 = driver.find_element("xpath","//textarea[@id='jsc_c_1n']")
                    except:
                        pass

        try:        
            tag1.send_keys(products.tag1)
            tag1.send_keys(Keys.RETURN)
            time.sleep(3)
        except:
            pass
        try:
            tag2 = driver.find_element(By.XPATH, "(//textarea[starts-with(@id, '«r')])[2]")
        except:
            try:
                tag2 = driver.find_element("xpath","//textarea[@id='jsc_c_1b']")
            except:
                try:
                    tag2 = driver.find_element("xpath","//textarea[@id='jsc_c_26']")
                except:
                    try:
                        tag2 = driver.find_element("xpath","//textarea[@id='jsc_c_1n']")
                    except:
                        pass
        try:        
            tag2.send_keys(products.tag2)
            tag2.send_keys(Keys.RETURN)
            time.sleep(3)
        except:
            pass
        try:
            tag3 = driver.find_element(By.XPATH, "(//textarea[starts-with(@id, '«r')])[2]")
        except:
            try:
                tag3 = driver.find_element("xpath","//textarea[@id='jsc_c_1b']")
            except:
                try:
                    tag3 = driver.find_element("xpath","//textarea[@id='jsc_c_26']")
                except:
                    try:
                        tag3 = driver.find_element("xpath","//textarea[@id='jsc_c_1n']")
                    except:
                        pass
        try:        
            tag3.send_keys(products.tag3)
            tag3.send_keys(Keys.RETURN)
            time.sleep(3)
        except:
            pass
        try:
            tag4 = driver.find_element(By.XPATH, "(//textarea[starts-with(@id, '«r')])[2]")
        except:
            try:
                tag4 = driver.find_element("xpath","//textarea[@id='jsc_c_1b']")
            except:
                try:
                    tag4 = driver.find_element("xpath","//textarea[@id='jsc_c_26']")
                except:
                    try:
                        tag4 = driver.find_element("xpath","//textarea[@id='jsc_c_1n']")
                    except:
                        pass
        try:        
            tag4.send_keys(products.tag4)
            tag4.send_keys(Keys.RETURN)
            time.sleep(3)
        except:
            pass
        try:
            tag5 = driver.find_element(By.XPATH, "(//textarea[starts-with(@id, '«r')])[2]")
        except:
            try:
                tag5 = driver.find_element("xpath","//textarea[@id='jsc_c_1b']")
            except:
                try:
                    tag5 = driver.find_element("xpath","//textarea[@id='jsc_c_26']")
                except:
                    try:
                        tag5 = driver.find_element("xpath","//textarea[@id='jsc_c_1n']")
                    except:
                        pass
        try:        
            tag5.send_keys(products.tag5)
            tag5.send_keys(Keys.RETURN)
            time.sleep(3)
        except:
            pass

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
    driver.quit()
    time.sleep(10)

