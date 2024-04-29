from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from reporting.locators import Xpath_locators
from reporting.locators import Class_locators
import time

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 10)

driver.get("https://uat.app.worklenz.com/auth")
driver.maximize_window()


def main():
    login()
    reporting()


def login():
    wait.until(EC.visibility_of_element_located((By.XPATH, Xpath_locators.email_xpath))).send_keys(
        "ncsdn@v.com")
    wait.until(EC.visibility_of_element_located((By.XPATH, Xpath_locators.password_xpath))).send_keys(
        "ceyDigital#00")
    wait.until(EC.visibility_of_element_located((By.XPATH, Xpath_locators.login_btn_xpath))).click()


def reporting():
    wait.until(EC.visibility_of_element_located((By.XPATH, Xpath_locators.reporting_xpath))).click()
    sider = wait.until(EC.visibility_of_element_located((By.TAG_NAME, "nz-sider")))
    sider_wait = WebDriverWait(sider, 20)
    s = sider_wait.until(EC.visibility_of_all_elements_located((By.TAG_NAME, "li")))
    print(len(s))



main()
