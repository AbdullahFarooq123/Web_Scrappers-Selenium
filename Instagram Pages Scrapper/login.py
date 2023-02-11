import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class Login:
    def __init__(self, driver, username, password):
        self.driver = driver
        self.username = username
        self.password = password

    def signin(self, wait):
        self.driver.get('https://www.instagram.com/accounts/login/?source=auth_switcher')
        time.sleep(2)
        user_name_field = WebDriverWait(self.driver, wait).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#loginForm > div > div:nth-child(1) > div > label > input')))
        user_name_field.click()
        user_name_field.send_keys(self.username)
        login_url = self.driver.current_url
        time.sleep(2)
        password_field = self.driver.find_element_by_css_selector('#loginForm > div > div:nth-child(2) > div > label > input')
        password_field.click()
        password_field.send_keys(self.password)
        time.sleep(2)
        login_btn = self.driver.find_element_by_css_selector('#loginForm > div > div:nth-child(3) > button > div')
        login_btn.click()
        time.sleep(10)
        current_url = self.driver.current_url
        if login_url == current_url or 'login_attempt' in current_url:
            raise 'Login failed'

