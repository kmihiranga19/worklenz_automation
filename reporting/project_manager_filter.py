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
    wait.until(EC.visibility_of_element_located((By.XPATH, Xpath_locators.reporting_projects_xpath))).click()


def project_manger_filed_check():
    head_wrapper = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "ant-card-head-wrapper")))
    head_wrapper_wait = WebDriverWait(head_wrapper, 10)
    button = head_wrapper_wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "button")))[4]
    button_wait = WebDriverWait(button, 10)
    button_wait.until(EC.visibility_of_all_elements_located((By.TAG_NAME, "span")))[1].click()
    show_filed_items_menu = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "ant-dropdown-menu-vertical")))
    show_filed_items_menu_wait = WebDriverWait(show_filed_items_menu, 10)
    manger_checkbox = show_filed_items_menu_wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "ant-dropdown-menu-item")))[-1]
    manger_checkbox_class_name = manger_checkbox.get_attribute("class")
    if "ant-checkbox-wrapper-checked" not in manger_checkbox_class_name:
        manger_checkbox.click()

    else:
        button.click()


def get_project_mangers_projects():
    managers_details = []

    table = wait.until(EC.visibility_of_element_located((By.TAG_NAME, "tbody")))
    time.sleep(2)
    rows = table.find_elements(By.TAG_NAME, "tr")
    for index, row in enumerate(rows):
        manager_details = {
            "project_name": "",
            "project_manager_name": ""
        }
        if index == 0:
            continue
        project_name = row.find_elements(By.TAG_NAME, "td")[0].text
        manager_name = row.find_elements(By.TAG_NAME, "td")[-1].text
        manager_details["project_name"] = project_name
        manager_details["project_manager_name"] = manager_name
        managers_details.append(manager_details)
        time.sleep(1)

    print(managers_details)


def filter_project_manager():
    head_wrapper = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "ant-card-head-wrapper")))
    head_wrapper_wait = WebDriverWait(head_wrapper, 10)
    button = head_wrapper_wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "button")))[4]
    button_wait = WebDriverWait(button, 10)
    button_wait.until(EC.visibility_of_all_elements_located((By.TAG_NAME, "span")))[1].click()
    drop_down_menu = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "ant-dropdown-menu-vertical")))
    drop_down_menu_wait = WebDriverWait(drop_down_menu, 10)
    project_manger = drop_down_menu_wait.until(EC.visibility_of_all_elements_located((By.TAG_NAME, "li")))[1]
    project_manger.click()


main()
project_manger_filed_check()
get_project_mangers_projects()
filter_project_manager()
