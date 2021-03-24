from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
import datetime as dt
import os
import sys
import time
import json

class TitleFlex:
    def __init__(self,driver):
        self.driver = driver
        

    @property
    def tf_username(self):
        username = os.environ["TITLEFLEX_USER"]
        assert username is not None
        return username

    @property
    def tf_password(self):
        password = os.environ["TITLEFLEX_PW"]
        assert password is not None
        return password


    def get_property_data(self,address):
        self.login()
        self.search_property(address)

        if self.is_complex_address():
            self.logout()
            return {"ERROR": "Multiple or zero results found"}

        property_data = {}

        property_data.update(self.get_apn())
        property_data.update(self.get_owners())
        property_data.update(self.get_bedrooms())
        property_data.update(self.get_living_area())
        property_data.update(self.get_zillow_data())
        property_data.update(self.get_realtor_data())

        self.logout()

        return property_data
        

    def login(self):
        username_form_id = "UserName"
        password_form_id = "Password"
        login_btn_path = "/html/body/section/div[1]/div[1]/div[2]/form/div[3]/div/div/div/button"
        proceed_btn_path = "/html/body/section/div[1]/div[3]/form/div[2]/div/div[3]//*[@id='btnSubmit']"
        
        self.driver.get("https://titleflex.datatree.com")

        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, username_form_id))).send_keys(self.tf_username)
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, password_form_id))).send_keys(self.tf_password)

        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, login_btn_path))).click()

        time.sleep(4)

    def is_complex_address(self):
        try:
            complex_path = "/html/body/div[1]/div[4]/section/div[3]/section/div[1]/div[2]/div[2]/div[1]/div[2]/div[1]/p"
            complex_field = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, complex_case_path)))
            return True
        except:
            return False

    def search_property(self,address):
        address_form_path = "/html/body/div[1]/div[2]/header/form/div[2]/div[2]/span[1]/span/input"
        
        address_form = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, address_form_path)))
        address_form.send_keys(address)
        address_form.send_keys(Keys.RETURN)

    def handle_popups(self):
        cookie_btn_id = "ccpa-gotit"
        popup_path = "/html/body/div[10]/div/div/div[3]/button"
        
        cookie_btn = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.ID, cookie_btn_id)))
        cookie_btn.click()
        
        popup_btn = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, popup_path)))
        popup_btn.click()

    def get_apn(self):
        apn_path = "/html/body/div[1]/div[4]/section/div[3]/section/div[1]/div[2]/div[2]/div[2]/div/div/div[1]/div[2]/div[3]/div[1]/div/span"
        apn = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, apn_path))).text
        return {"APN": apn}

    def get_living_area(self):
        living_area_field_path = "/html/body/div[1]/div[4]/section/div[3]/section/div[1]/div[2]/div[2]/div[2]/div/div/div[1]/div[2]/div[3]/div[3]/div[3]/span"
        living_area_field = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, living_area_field_path))).text
        living_area = int(living_area_field.split()[0].replace(',', ''))
        return  {"Square Footage": living_area}

    def get_bedrooms(self):
        bedrooms,bathrooms = 0,0
        try:
            bedrooms_field_path = "/html/body/div[1]/div[4]/section/div[3]/section/div[1]/div[2]/div[2]/div[2]/div/div/div[1]/div[2]/div[3]/div[3]/div[1]/span"
            bedrooms_field = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, bedrooms_field_path))).text
            bedrooms = int(bedrooms_field)

            bathrooms_field_path = "/html/body/div[1]/div[4]/section/div[3]/section/div[1]/div[2]/div[2]/div[2]/div/div/div[1]/div[2]/div[3]/div[3]/div[2]/span"
            bathrooms_field = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, bathrooms_field_path))).text
            bathrooms = sum([int(x.strip()) for x in bathrooms_field.split("/")])
        except:
            pass
        
        return {"Bedrooms": bedrooms, "Bathrooms":bathrooms}

    def get_zillow_data(self):
        #show links dropdown on titleflex
        links_element_path = '/html/body/div[1]/div[4]/section/div[3]/section/div[1]/div[2]/div[1]/div/ul/li[11]/a'
        links_element = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, links_element_path)))
        ActionChains(self.driver).move_to_element(links_element).perform()

        #click zillow link button
        zillow_path = "/html/body/div[1]/div[4]/section/div[3]/section/div[1]/div[2]/div[1]/div/ul/li[11]/ul/li[1]"
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, zillow_path))).click()
        time.sleep(3)

        #switch to zillow window
        self.driver.switch_to.window(self.driver.window_handles[1])
        time.sleep(1)

        #get zestimate
        zestimate_paths = [
                        "/html/body/div[1]/div[6]/div[1]/div[1]/div/div/div[3]/div/div/div/div[2]/div[3]/div[2]/div/p/span[2]/span[2]/span[2]",
                        "/html/body/div[1]/div[6]/div[1]/div[1]/div/div/div[3]/div/div/div/div[2]/div[4]/div[2]/div/p/span[3]/span[2]/span[2]",
                        "/html/body/div[1]/div[6]/div[1]/div[1]/div/div/div[3]/div/div/div/div[2]/div[4]/div[2]/div/div[3]/p/span[2]/span[2]/span[2]",
                        "/html/body/div[1]/div[6]/div[1]/div[1]/div/div/div[3]/div/div/div/div[2]/div[3]/div[2]/div/p/span[3]/span[2]/span[2]",
                        "/html/body/div[1]/div[6]/div[1]/div[1]/div/div/div[3]/div/div/div/div[2]/div[4]/div[2]/div/p/span[2]/span[2]/span[2]"
                    ]
        #0 is default value to be returned if zestimate not available
        zestimate = 0
        for zestimate_path in zestimate_paths:
            try:
                zestimate_field = WebDriverWait(self.driver, 2).until(EC.element_to_be_clickable((By.XPATH, zestimate_path))).text
                zestimate = int(zestimate_field.replace("$","").replace(",",""))
                break
            except:
                pass

        #close out zillow window
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])

        return {"Market Value": zestimate}

    def get_realtor_data(self):
        links_element_path = '/html/body/div[1]/div[4]/section/div[3]/section/div[1]/div[2]/div[1]/div/ul/li[11]/a'
        links_element = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, links_element_path)))
        ActionChains(self.driver).move_to_element(links_element).perform()

        realtor_path = "/html/body/div[1]/div[4]/section/div[3]/section/div[1]/div[2]/div[1]/div/ul/li[11]/ul/li[3]"
        self.driver.find_element_by_xpath(realtor_path).click()
        time.sleep(3)
        self.driver.switch_to.window(self.driver.window_handles[1])


        public_records_element_id = "ldp-detail-public-records"
        public_records_element = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, public_records_element_id)))
        public_records = public_records_element.text.split("\n")[1:]
        public_records_data = {x.split(":")[0]:x.split(":")[1].strip() for x in public_records if len(x.split(":")) > 1}
        
        try:
            year_built = int(public_records_data["Year built"])
        except:
            year_built = None
        try:
            stories = int(public_records_data["Stories"])
        except:
            stories = None



        additions,assessment,prior_assessment = -1,-1,-1
        try:
            tax_records_element_id = "ldp-history-taxes"
            tax_records_element = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, tax_records_element_id)))
            latest_tax_records = tax_records_element.text.split("\n")[2:][:2]
            try:
                additions = int(latest_tax_records[0].split("+")[1].split()[0].replace("$","").replace(",","").strip())
            except:
                print("additions field data: ",latest_tax_records[0].split("+")[1].split()[0])
                pass
            try:
                assessment = int(latest_tax_records[0].split()[-1].replace("$","").replace(",","").strip())
            except:
                print("assessment field data: ",latest_tax_records[0].split()[-1])
                pass
            try:
                prior_assessment = int(latest_tax_records[1].split()[-1].replace("$","").replace(",","").strip())
            except:
                print("prior_assessment field data: ",latest_tax_records[1].split()[-1])
                pass
            if additions+assessment+prior_assessment == -3:
                raise Exception("No values were available")
        except Exception as error:
            print(error)
            


        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])  

        return {"Assessed Value": assessment,
                "Prior Assessed Value": prior_assessment,
                "Additions":additions,
                "Year Built":year_built,
                "Stories":stories}

    def get_owners(self):
        owners_path = "/html/body/div[1]/div[4]/section/div[3]/section/div[1]/div[2]/div[2]/div[2]/div/div/div[1]/div[2]/div[2]"
        owners = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, owners_path))).get_attribute("title")
        owners = [name.strip() for name in owners.split("/")]
        return {"Owners":owners}

    def logout(self):
        profile_dropdown_path = "/html/body/div[1]/div[2]/header/div/div/ul/li/div[2]/a"
        logout_btn_path = "/html/body/div[1]/div[2]/header/div/div/ul/li/ul/li[8]/a"

        time.sleep(2)
        actions = ActionChains(self.driver)
        profile_dropdown_btn = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, profile_dropdown_path)))
        actions.move_to_element(profile_dropdown_btn).perform()

        logout_btn = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, logout_btn_path)))
        actions.move_to_element(logout_btn).perform()
        logout_btn.click()