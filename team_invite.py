import random
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from faker import Faker

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
    wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='Email']"))).send_keys(
        "ncsdn@v.com")
    wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='Password']"))).send_keys(
        "ceyDigital#00")
    wait.until(EC.visibility_of_element_located((By.XPATH, "//span[normalize-space()='Log in']"))).click()


def header_team_invite_btn():
    invite_btn = wait.until(EC.visibility_of_element_located((By.XPATH, "//span[normalize-space()='Invite']")))
    invite_btn.click()


def add_team_member():
    click_email = wait.until(EC.visibility_of_element_located((By.XPATH,
                                                               "//div[@id='cdk-overlay-0']/div/div[2]/div/div/div[2]/nz-spin/div/form/nz-form-item/nz-form-control/div/div/nz-select/nz-select-top-control")))
    click_email.click()
    enter_email = wait.until(EC.visibility_of_element_located((By.XPATH,
                                                               "//div[@id='cdk-overlay-0']/div/div[2]/div/div/div[2]/nz-spin/div/form/nz-form-item/nz-form-control/div/div/nz-select/nz-select-top-control/nz-select-search/input")))
    random_email = fake.email()
    enter_email.send_keys(random_email, Keys.ENTER)
    click_job_title = wait.until(EC.visibility_of_element_located((By.XPATH,
                                                                   "//div[@id='cdk-overlay-0']/div/div[2]/div/div/div[2]/nz-spin/div/form/worklenz-job-titles-autocomplete/form/nz-form-item/nz-form-control/div/div/input")))
    click_job_title.click()
    enter_job_title = wait.until(EC.visibility_of_element_located((By.XPATH,
                                                                   "//div[@id='cdk-overlay-0']/div/div[2]/div/div/div[2]/nz-spin/div/form/worklenz-job-titles-autocomplete/form/nz-form-item/nz-form-control/div/div/input")))
    enter_job_title.send_keys("Software engineer", Keys.ENTER)
    click_access = wait.until(EC.visibility_of_element_located((By.XPATH,
                                                                "//div[@id='cdk-overlay-0']/div/div[2]/div/div/div[2]/nz-spin/div/form/nz-form-item[2]/nz-form-control/div/div/nz-select/nz-select-top-control/nz-select-item")))
    click_access.click()
    dropdown = wait.until(EC.visibility_of_element_located((By.TAG_NAME, "nz-option-container")))
    dropdown_wait = WebDriverWait(dropdown, 10)
    selects = dropdown_wait.until(EC.visibility_of_all_elements_located((By.TAG_NAME, "nz-option-item")))
    no = random.randint(0, 1)
    selects[no].click()
    wait.until(EC.visibility_of_element_located((By.XPATH, "//span[normalize-space()='Add to team']"))).click()
    time.sleep(6)


def go_to_team_members_list():
    wait.until(EC.visibility_of_element_located((By.XPATH, "//li[5]"))).click()
    profile_details = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "profile-details-dropdown")))
    profile_details_wait = WebDriverWait(profile_details, 10)
    profile_details_wait.until(EC.visibility_of_all_elements_located((By.TAG_NAME, "li")))[1].click()
    sider = wait.until(EC.visibility_of_element_located((By.TAG_NAME, "nz-sider")))
    sider_wait = WebDriverWait(sider, 10)
    sider_wait.until(EC.visibility_of_any_elements_located((By.TAG_NAME, "li")))[8].click()


def team_members_list():
    t_body = wait.until(EC.visibility_of_element_located((By.TAG_NAME, "tbody")))
    t_body_wait = WebDriverWait(t_body, 10)
    rows = t_body_wait.until(EC.visibility_of_all_elements_located((By.TAG_NAME, "tr")))
    for row in rows:
        row_wait = WebDriverWait(row, 10)
        need_column = row_wait.until(EC.visibility_of_all_elements_located((By.TAG_NAME, "td")))[2]
        need_column_wait = WebDriverWait(need_column, 10)
        span = need_column_wait.until(EC.visibility_of_element_located((By.TAG_NAME, "span")))
        time.sleep(3)
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
            print(final_text)

        else:
            print(span.text.strip())

        



        time.sleep(1)


main()
# header_team_invite_btn()
# add_team_member()
go_to_team_members_list()
team_members_list()
