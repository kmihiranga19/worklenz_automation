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
    manger_checkbox = \
        show_filed_items_menu_wait.until(
            EC.visibility_of_all_elements_located((By.CLASS_NAME, "ant-dropdown-menu-item")))[
            -1]
    manger_checkbox_class_name = manger_checkbox.get_attribute("class")

    if "ant-checkbox-wrapper-checked" not in manger_checkbox_class_name:
        manger_checkbox.click()

    else:
        button.click()


def get_filtering_project_manager():
    not_need_span = '<input type="checkbox" class="ant-checkbox-input ng-untouched ng-pristine ng-valid"><span class="ant-checkbox-inner"></span>'
    head_wrapper = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "ant-card-head-wrapper")))
    head_wrapper_wait = WebDriverWait(head_wrapper, 10)
    button = head_wrapper_wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "button")))[3]
    button_wait = WebDriverWait(button, 10)
    button_wait.until(EC.visibility_of_all_elements_located((By.TAG_NAME, "span")))[1].click()
    time.sleep(4)
    drop_down_menu = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "ant-dropdown-menu-vertical")))
    drop_down_menu_wait = WebDriverWait(drop_down_menu, 20)
    project_manger = drop_down_menu_wait.until(EC.visibility_of_all_elements_located((By.TAG_NAME, "li")))[1]
    project_manger_wait = WebDriverWait(project_manger, 20)
    span_tags = project_manger_wait.until(EC.visibility_of_all_elements_located((By.TAG_NAME, "span")))
    for span_tag in span_tags:
        if span_tag.get_attribute('innerHTML') != "":
            if span_tag.get_attribute('innerHTML') == not_need_span:
                continue
            project_manager_name = span_tag.get_attribute('innerHTML')
            return project_manager_name.strip()


def get_project_manager_projects(filtered_manager_name):
    projects_details = []

    table = wait.until(EC.visibility_of_element_located((By.TAG_NAME, "tbody")))
    time.sleep(2)
    rows = table.find_elements(By.TAG_NAME, "tr")
    for index, row in enumerate(rows):
        project_details = {
            "project_name": "",
            "project_manager_name": ""
        }
        if index == 0:
            continue
        project_name = row.find_elements(By.TAG_NAME, "td")[0].text
        manager_cell = row.find_elements(By.TAG_NAME, "td")[-1]
        try:
            manager_cell.find_element(By.TAG_NAME, "worklenz-na")

        except NoSuchElementException:
            manager = manager_cell.find_elements(By.TAG_NAME, "span")[1].text
            manager_name = manager.strip()
            if manager_name == filtered_manager_name:
                project_details["project_name"] = project_name
                project_details["project_manager_name"] = manager_name
                projects_details.append(project_details)
        time.sleep(1)

    return projects_details


def filtering_project_manager():
    drop_down_menu = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "ant-dropdown-menu-vertical")))
    drop_down_menu_wait = WebDriverWait(drop_down_menu, 20)
    select_project_manger = drop_down_menu_wait.until(EC.visibility_of_all_elements_located((By.TAG_NAME, "li")))[1]
    select_project_manger.click()


def get_projects_after_filtering():
    filtered_projects_details = []

    table = wait.until(EC.visibility_of_element_located((By.TAG_NAME, "tbody")))
    time.sleep(2)
    rows = table.find_elements(By.TAG_NAME, "tr")
    for index, row in enumerate(rows):
        project_details = {
            "project_name": "",
            "project_manager_name": ""
        }
        if index == 0:
            continue
        project_name = row.find_elements(By.TAG_NAME, "td")[0].text
        manager_cell = row.find_elements(By.TAG_NAME, "td")[-1]
        manager_name = manager_cell.find_elements(By.TAG_NAME, "span")[1].text
        project_details["project_name"] = project_name
        project_details["project_manager_name"] = manager_name
        filtered_projects_details.append(project_details)
        time.sleep(1)

    return filtered_projects_details


def check_filter_work_correctly(p_manager_projects, p_filtered_projects):
    for p_manager_project in p_manager_projects:
        for p_filtered_project in p_filtered_projects:
            manager_projects_name = p_manager_project["project_name"]
            manager_projects_manager_name = p_manager_project["project_manager_name"]
            filtered_projects_name = p_filtered_project["project_name"]
            filtered_projects_manager_name = p_filtered_project["project_manager_name"]

            if (manager_projects_name.strip() == filtered_projects_name.strip()) & (
                    manager_projects_manager_name.strip() == filtered_projects_manager_name.strip()):
                print(f'{manager_projects_name} successfully filtered')
            else:
                print("Filter not working correctly")



main()
project_manger_filed_check()
filtered_manger_name = get_filtering_project_manager()
manager_projects = get_project_manager_projects(filtered_manger_name)
filtering_project_manager()
filtered_projects = get_projects_after_filtering()
check_filter_work_correctly(manager_projects, filtered_projects)
