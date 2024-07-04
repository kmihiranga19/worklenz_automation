import time
from faker import Faker
from selenium import webdriver
import pytest
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Test_change_password:
    faker = Faker()
    no = faker.random_int()

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

    def change_password(self, current_psw, new_psw, new_current_psw):
        self.wait.until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, "input[placeholder='Enter your current password']"))).send_keys(current_psw)
        self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "input[placeholder='New Password']"))).send_keys(
            new_psw)
        self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "input[placeholder='Confirm New Password']"))).send_keys(
            new_current_psw)
        self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "button[type='submit']"))).click()

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

    def test_verify_change_password_page(self):
        self.login("fddf@d.com", "ceyDigital#00")
        time.sleep(5)
        self.driver.get("https://uat.app.worklenz.com/worklenz/settings/password")
        try:
            self.wait.until(
                EC.visibility_of_element_located((By.XPATH, "//label[normalize-space()='Confirm New Password']")))

        except NoSuchElementException:
            pytest.fail("Test case fail: Verify change password page")

    def test_verify_user_able_change_password(self):

        current_password = 'ceyDigital#00'
        new_password = 'ceyDigital#'
        self.login("fdd@m.com", current_password)
        time.sleep(5)
        self.driver.get("https://uat.app.worklenz.com/worklenz/settings/password")
        self.change_password(current_password, new_password, new_password)
        current_password = new_password
        self.account_log_out()
        self.login("fdd@m.com", current_password)

        try:
            self.wait.until(EC.visibility_of_element_located((By.XPATH, "//strong[normalize-space()='Home']")))

        except NoSuchElementException:
            pytest.fail("Test case: test verify user able change password")

    def test_verify_user_unable_change_psw_with_invalid_current_psw(self):
        wrong_current_password = 'wrongPsw00'
        current_password = 'ceyDigital#00'
        new_password = 'ceyDigital#18'
        self.login("fddf@d.com", current_password)
        time.sleep(5)
        self.driver.get("https://uat.app.worklenz.com/worklenz/settings/password")
        self.change_password(wrong_current_password, new_password, new_password)
        self.account_log_out()
        self.login("fddf@d.com", new_password)
        try:
            self.wait.until(EC.visibility_of_element_located((By.XPATH, "//span[normalize-space()='Log in']")))

        except NoSuchElementException:
            pytest.fail("Test case: test verify user unable change psw with invalid current password")

    def test_verify_user_unable_change_psw_with_invalid_confirm_new_psw(self):
        current_password = 'ceyDigital#00'
        new_password = 'ceyDigital#18'
        confirm_new_password = 'ceyDigital#20'
        self.login("fddf@d.com", current_password)
        time.sleep(5)
        self.driver.get("https://uat.app.worklenz.com/worklenz/settings/password")
        self.change_password(current_password, new_password, confirm_new_password)
        self.account_log_out()
        self.login("fddf@d.com", new_password)
        try:
            self.wait.until(EC.visibility_of_element_located((By.XPATH, "//span[normalize-space()='Log in']")))

        except NoSuchElementException:
            pytest.fail("Test case: test verify user unable change psw with invalid current password")
