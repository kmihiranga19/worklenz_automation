from selenium import webdriver
import pytest
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Test_login:
    def setup_method(self):
        options = webdriver.ChromeOptions()
        options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 20)
        self.driver.get("https://uat.app.worklenz.com/auth/login")
        self.driver.maximize_window()

    def test_verify_able_login_with_credentials(self):
        self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[placeholder='Email']"))).send_keys(
            "ceyare4516@mliok.com")
        self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[placeholder='Password']"))).send_keys(
            "ceyDigital#00")
        self.wait.until(EC.visibility_of_element_located((By.XPATH, "//span[normalize-space()='Log in']"))).click()

        try:
            self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "logo-holder")))

        except NoSuchElementException:
            pytest.fail("Test case fail: Verify user unable login with correct credentials")

    def test_verify_unable_login_with_invalid_email(self):
        self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[placeholder='Email']"))).send_keys(
            "ceyare4516mliok")
        self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[placeholder='Password']"))).send_keys(
            "ceyDigital#00")
        self.wait.until(EC.visibility_of_element_located((By.XPATH, "//span[normalize-space()='Log in']"))).click()

        try:
            self.wait.until(
                EC.visibility_of_element_located((By.XPATH, "//div[normalize-space()='Please input your email!']")))

        except NoSuchElementException:
            pytest.fail("Test case fail: Verify user able login with invalid email")

    def test_verify_unable_login_with_invalid_password(self):
        self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[placeholder='Email']"))).send_keys(
            "ceyare4516@mliok")
        self.wait.until(EC.visibility_of_element_located((By.XPATH, "//span[normalize-space()='Log in']"))).click()

        try:
            self.wait.until(
                EC.visibility_of_element_located((By.XPATH, "//div[normalize-space()='Please input your Password!']")))

        except NoSuchElementException:
            pytest.fail("Test case fail: Verify user able login with invalid password")

    def test_verify_unable_login_with_wrong_credentials(self):
        self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[placeholder='Email']"))).send_keys(
            "ceyare4516@mliok.com")
        self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[placeholder='Password']"))).send_keys(
            "ceyDigital")
        self.wait.until(EC.visibility_of_element_located((By.XPATH, "//span[normalize-space()='Log in']"))).click()

        try:
            self.wait.until(
                EC.visibility_of_element_located((By.XPATH, "//div[normalize-space()='Login failed!']")))
        except NoSuchElementException:
            pytest.fail("Test case fail: Verify user able login with wrong password")


