import time
from faker import Faker
from selenium import webdriver
import pytest
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Test_change_password:

    def setup_method(self):
        options = webdriver.ChromeOptions()
        options.add_experimental_option("detach", True)
        prefs = {"profile.default_content_setting_values.notifications": 2}
        options.add_experimental_option("prefs", prefs)
        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 20)
        self.driver.get("https://uat.app.worklenz.com/auth/login")
        self.driver.maximize_window()

    def login(self, email, password):
        self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "input[placeholder='Email']"))).send_keys(email)
        self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "input[placeholder='Password']"))).send_keys(
            password)
        self.wait.until(EC.visibility_of_element_located((By.XPATH, "//span[normalize-space()='Log in']"))).click()

        return password

    def test_verify_change_password_page(self):
        self.login("bsdcsd@v.com", "ceyDigital#00")
        time.sleep(5)
        self.driver.get("https://uat.app.worklenz.com/worklenz/settings/password")
        try:
            self.wait.until(
                EC.visibility_of_element_located((By.XPATH, "//label[normalize-space()='Confirm New Password']")))

        except NoSuchElementException:
            pytest.fail("Test case fail: Verify change password page")

    def test_verify_user_able_change_password(self):
        faker = Faker()
        no = faker.number()
        current_password = 'ceyDigital#03'
        new_password = 'ceyDigital#' + no
        print(new_password)
        self.login("bsdcsd@v.com", current_password)
        time.sleep(5)
        self.driver.get("https://uat.app.worklenz.com/worklenz/settings/password")

        self.wait.until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, "input[placeholder='Enter your current password']"))).send_keys(current_password)
        self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "input[placeholder='New Password']"))).send_keys(new_password)
        self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "input[placeholder='Confirm New Password']"))).send_keys(
            new_password)
        self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "button[type='submit']"))).click()
        current_password = new_password
        wl_header = self.wait.until(EC.visibility_of_element_located((By.TAG_NAME, "worklenz-header")))
        wl_header_wait = WebDriverWait(wl_header, 10)
        left_header = wl_header_wait.until(EC.visibility_of_element_located((By.TAG_NAME, "ul")))[1]
        left_header_wait = WebDriverWait(left_header, 10)
        left_header_wait.until(EC.visibility_of_element_located((By.TAG_NAME, "li")))[-1].click()

