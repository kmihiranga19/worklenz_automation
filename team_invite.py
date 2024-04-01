import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from faker import Faker

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 10)
fake = Faker()

driver.get("https://uat.app.worklenz.com/auth")
driver.maximize_window()


def main():
    login()


def login():
    wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='Email']"))).send_keys(
        "bsdcsd@v.com")
    wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='Password']"))).send_keys(
        "ceyDigital#00")
    wait.until(EC.visibility_of_element_located((By.XPATH, "//span[normalize-space()='Log in']"))).click()
    time.sleep(10)


def header_team_invite_btn():
    invite_btn = wait.until(EC.visibility_of_element_located((By.XPATH,
                                                              "/html/body/worklenz-root/worklenz-layout/nz-spin/div/nz-layout/nz-header/worklenz-header/div[2]/div/div/ul/li[2]")))
    invite_btn.click()
    time.sleep(5)


def add_team_member():
    click_email = wait.until(EC.visibility_of_element_located((By.XPATH,
                                                               "//div[@id='cdk-overlay-0']/div/div[2]/div/div/div[2]/nz-spin/div/form/nz-form-item/nz-form-control/div/div/nz-select/nz-select-top-control")))
    click_email.click()
    time.sleep(1)
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
    click_access = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@id='cdk-overlay-0']/div/div[2]/div/div/div[2]/nz-spin/div/form/nz-form-item[2]/nz-form-control/div/div/nz-select/nz-select-top-control/nz-select-item")))
    click_access.click()
    dropdown = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "ant-select-dropdown")))
    selects = dropdown.find_elements(By.CLASS_NAME, "ant-select-item")
    no = random.randint(0, 1)
    selects[no].click()


main()
header_team_invite_btn()
add_team_member()
