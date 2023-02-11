import time

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from login import Login
from pages import GetPages

chrome_options = Options()
# prefs = {"profile.default_content_setting_values.notifications": 2}
# chrome_options.add_argument('--disable-notifications')
# chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
# chrome_options.add_experimental_option("prefs", prefs)
driver = None
try:
    driver = webdriver.Chrome(service=Service('../chromedriver.exe'), options=chrome_options)
    login_error = 0
    network_error = 0
    login = Login(driver=driver, username="abdullahfarooq583", password="Abdullah123")
    wait = 10
    while True:
        try:
            login.signin(wait)
            print("Login successful")
            break
        except TimeoutException:
            wait += 5
            network_error += 1
            if network_error > 5:
                print('Network Error')
                driver.close()
                exit(1)
        except Exception:
            login_error += 1
            if login_error > 1:
                print('Login error user-name or password-incorrect')
                driver.close()
                exit(1)
except (FileNotFoundError, Exception):
    print("Chromedriver not found")
    driver.close()
    exit(1)
pages = [
    'https://www.instagram.com/dzakysz/',
    'https://www.instagram.com/ak______010/',
    'https://www.instagram.com/__hell_lover_/',
    'https://www.instagram.com/morgan.kkjj/',
    'https://www.instagram.com/tamiresx___/',
    'https://www.instagram.com/parsoya594/',
    'https://www.instagram.com/its_priya_949/',
    'https://www.instagram.com/leofatrio/',
    'https://www.instagram.com/sonbaharr044/',
    'https://www.instagram.com/sharmapranav6/',
    'https://www.instagram.com/saeedn783/',
    'https://www.instagram.com/lowking25_priv/',
    'https://www.instagram.com/pritampaglachoda/',
]
wait = 5
index = 0
error = 0
while index < len(pages):
    get_pages = GetPages(driver, pages[index])
    time.sleep(wait)
    flag = get_pages.get_num_followers(wait)
    if not flag[0]:
        wait += 2
        error += 1
        if not flag[1]:
            print(
                str(index + 1) + " : Cant retrieve Followers At " + get_pages.driver.current_url + " : " + (
                    " Page Error"))
            wait = 5
            error = 0
            index += 1
        elif error > 5:
            print(
                str(index + 1) + " : Cant retrieve Followers At " + get_pages.driver.current_url + " : " + (
                    " Network Error!"))
            wait = 5
            error = 0
            index += 1

    else:
        index += 1
        wait = 5
        error = 0
        print(str(index) + " : FOLLOWERS AT " + get_pages.driver.current_url + " : " + str(get_pages.no_of_followers))
    time.sleep(wait)
driver.close()
