import random
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from faker import Faker
from locators import Xpath_locators, Class_locators

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 20)
fake = Faker()

driver.get("https://uat.app.worklenz.com/auth")
driver.maximize_window()


def main():
    login()


def login():
    wait.until(EC.visibility_of_element_located((By.XPATH, Xpath_locators.email_xpath))).send_keys(
        "ncsdn@v.com")
    wait.until(EC.visibility_of_element_located((By.XPATH, Xpath_locators.password_xpath))).send_keys(
        "ceyDigital#00")
    wait.until(EC.visibility_of_element_located((By.XPATH, Xpath_locators.login_btn_xpath))).click()


def header_team_invite_btn():
    invite_btn = wait.until(
        EC.visibility_of_element_located((By.XPATH, Xpath_locators.navigation_bar_invite_btn_xpath)))
    invite_btn.click()


def add_team_member():
    click_email = wait.until(
        EC.visibility_of_element_located((By.XPATH, Xpath_locators.member_invite_click_email_xpath)))
    click_email.click()
    enter_email = wait.until(
        EC.visibility_of_element_located((By.XPATH, Xpath_locators.member_invite_enter_email_xpath)))
    random_email = fake.email()
    enter_email.send_keys(random_email, Keys.ENTER)
    click_job_title = wait.until(
        EC.visibility_of_element_located((By.XPATH, Xpath_locators.member_invite_click_job_title_xpath)))
    click_job_title.click()
    enter_job_title = wait.until(
        EC.visibility_of_element_located((By.XPATH, Xpath_locators.member_invite_enter_job_title_xpath)))
    enter_job_title.send_keys("Software engineer", Keys.ENTER)
    click_access = wait.until(
        EC.visibility_of_element_located((By.XPATH, Xpath_locators.member_invite_click_access_xpath)))
    click_access.click()
    dropdown = wait.until(EC.visibility_of_element_located((By.TAG_NAME, "nz-option-container")))
    dropdown_wait = WebDriverWait(dropdown, 10)
    selects = dropdown_wait.until(EC.visibility_of_all_elements_located((By.TAG_NAME, "nz-option-item")))
    no = random.randint(0, 1)
    selects[no].click()
    wait.until(EC.visibility_of_element_located((By.XPATH, Xpath_locators.member_invite_add_team_xpath))).click()
    time.sleep(6)

    return random_email


def go_to_team_members_list():
    wait.until(EC.visibility_of_element_located((By.XPATH, "//li[5]"))).click()
    profile_details = wait.until(
        EC.visibility_of_element_located((By.CLASS_NAME, Class_locators.profile_details_class)))
    profile_details_wait = WebDriverWait(profile_details, 10)
    profile_details_wait.until(EC.visibility_of_all_elements_located((By.TAG_NAME, "li")))[1].click()
    sider = wait.until(EC.visibility_of_element_located((By.TAG_NAME, "nz-sider")))
    sider_wait = WebDriverWait(sider, 10)
    sider_wait.until(EC.visibility_of_any_elements_located((By.TAG_NAME, "li")))[8].click()


def team_members_list():
    members_list = []
    t_body = wait.until(EC.visibility_of_element_located((By.TAG_NAME, "tbody")))
    t_body_wait = WebDriverWait(t_body, 10)
    rows = t_body_wait.until(EC.visibility_of_all_elements_located((By.TAG_NAME, "tr")))
    for row in rows:
        email = ''
        row_wait = WebDriverWait(row, 10)
        need_column = row_wait.until(EC.visibility_of_all_elements_located((By.TAG_NAME, "td")))[2]
        need_column_wait = WebDriverWait(need_column, 10)
        span = need_column_wait.until(EC.visibility_of_element_located((By.TAG_NAME, "span")))
        time.sleep(2)
        small_tag_present = False
        try:
            small_tag = span.find_element(By.TAG_NAME, "small")
            if small_tag.is_displayed():
                small_tag_present = True
        except NoSuchElementException:
            pass

        if small_tag_present:
            small_tag = WebDriverWait(span, 10).until(EC.visibility_of_element_located((By.TAG_NAME, "small")))
            outer_text = span.text.strip()
            inner_text = small_tag.text.strip()
            final_text = outer_text.replace(inner_text, "").strip()
            email = final_text

        else:
            email = span.text.strip()

        members_list.append(email)
        time.sleep(1)

    return members_list


def check_invited_member_add_to_list(inv_member, members_list):
    for member_list in members_list:
        if inv_member == member_list:
            print(f"Successfully '{inv_member}' member add to team ")
            break

        else:
            print(f"{inv_member} not add to team")
            break


main()
header_team_invite_btn()
invited_member = add_team_member()
go_to_team_members_list()
members_list = team_members_list()
check_invited_member_add_to_list(invited_member, members_list)
