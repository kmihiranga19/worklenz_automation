import time
from faker import Faker
from selenium import webdriver
import pytest
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


class Test_forgot_password:
    faker = Faker()
    no = faker.random_int()

    def setup_method(self):
        options = webdriver.ChromeOptions()
        options.add_experimental_option("detach", True)
        prefs = {"profile.default_content_setting_values.notifications": 2}
        options.add_experimental_option("prefs", prefs)
        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 20)
        self.driver.get("https://uat.app.worklenz.com/auth/signup")
        self.driver.maximize_window()

    def login(self, email, password):
        self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "input[placeholder='Email']"))).send_keys(email)
        self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "input[placeholder='Password']"))).send_keys(
            password)
        self.wait.until(EC.visibility_of_element_located((By.XPATH, "//span[normalize-space()='Log in']"))).click()

    def account_log_out(self):
        wl_header = self.wait.until(EC.visibility_of_element_located((By.TAG_NAME, "worklenz-header")))
        wl_header_wait = WebDriverWait(wl_header, 10)
        left_header = wl_header_wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "top-nav-ul-secondary")))
        left_header_wait = WebDriverWait(left_header, 10)
        left_header_wait.until(EC.visibility_of_all_elements_located((By.TAG_NAME, "li")))[-1].click()
        drop_down = self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "profile-details-dropdown")))
        drop_down_wait = WebDriverWait(drop_down, 10)
        drop_down_wait.until(EC.visibility_of_all_elements_located((By.TAG_NAME, "li")))[2].click()
        self.wait.until(EC.visibility_of_element_located((By.XPATH, "//span[normalize-space()='OK']"))).click()

    def create_new_user_account(self):
        self.driver.get("https://temp-mail.org/en/")
        time.sleep(10)
        self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "button[id='click-to-copy']"))).click()
        self.driver.back()
        self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[id='full-name']"))).send_keys("Test_user")
        self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[id='email']"))).send_keys(Keys.CONTROL + 'v')
        self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[id='password']"))).send_keys("ceyDigital#00")
        self.wait.until(EC.visibility_of_element_located((By.XPATH, "//span[normalize-space()='Sign up']"))).click()
        self.wait.until(EC.visibility_of_element_located((By.TAG_NAME, 'input'))).send_keys("Project")
        self.wait.until(EC.visibility_of_element_located(By.XPATH, ""))

    def test_b(self):
        self.create_new_user_account()
