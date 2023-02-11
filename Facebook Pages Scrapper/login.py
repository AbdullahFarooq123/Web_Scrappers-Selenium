import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.webdriver import WebDriver


class Login:
    def __init__(self, driver: WebDriver, username: str, password: str):
        self.driver = driver
        self.username = username
        self.password = password

    def signin_fb(self, wait):
        self.driver.get('https://www.facebook.com/login')
        user_name_field = WebDriverWait(self.driver, wait).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#email')))
        user_name_field.click()
        login_url = self.driver.current_url
        user_name_field.send_keys(self.username)
        password_field = self.driver.find_element(By.CSS_SELECTOR, '#pass')
        password_field.click()
        password_field.send_keys(self.password)
        login_btn = self.driver.find_element(By.CSS_SELECTOR, '#loginbutton')
        login_btn.click()
        time.sleep(5)
        current_url = self.driver.current_url
        if login_url == current_url or 'login_attempt' in current_url:
            raise 'Login failed'
