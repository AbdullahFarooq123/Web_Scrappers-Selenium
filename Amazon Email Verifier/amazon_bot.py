import math
import time

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from bs4 import BeautifulSoup
import random
from colorama import Fore
import threading

valid_mails = []
invalid_mails = []


def validate_emails(start_index, end_index, proxy):
    global valid_mails
    global invalid_mails
    chrome_options = Options()
    prefs = {"profile.default_content_setting_values.notifications": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_argument("--headless")
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    if 'y' in option:
        chrome_options.add_argument('--proxy-server=http://' + proxy)
    login_page = 'https://www.amazon.com/ap/signin?openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.com%2F%3Fref_%3Dnav_signin&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=usflex&openid.mode=checkid_setup&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&'
    driver = None
    try:
        driver = webdriver.Chrome(service=Service('chromedriver.exe'), options=chrome_options)
        time.sleep(10)
    except (FileNotFoundError, Exception):
        print("Chromedriver not found")
        driver.close()
        exit(1)
    # valid_mails = open('valid'+threading.currentThread().name+'.txt', 'w')
    # invalid_mails = open('invalid'+threading.currentThread().name+'.txt', 'w')
    wait = 10
    error = 0
    index = start_index
    while index < end_index:
        driver.get(login_page)
        try:
            email_field = WebDriverWait(driver, wait).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#ap_email')))
            email_field.click()
            email_field.send_keys(emails[index].strip())
            continue_btn = driver.find_element(By.CSS_SELECTOR, '#continue')
            continue_btn.click()
            body = WebDriverWait(driver, wait).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'body')))
            html = BeautifulSoup(body.get_attribute('innerHTML'), 'html.parser')
            alerts = html.find_all('span', {'class': 'a-list-item'})
            if len(alerts) > 0:
                invalid_mails.append(emails[index].strip())
                print(Fore.RED + emails[index].strip() + " : " + "INVALID")
            else:
                valid_mails.append(emails[index].strip())
                print(Fore.GREEN + emails[index].strip() + " : " + "VALID")
            index += 1
        except TimeoutException as network_error:
            wait += 2
            error += 1
            if error > 5:
                print("Network Error")
                break
        except:
            pass
    # threads[int(threading.currentThread().name)] = False
    driver.close()


def write_to_file():
    global valid_mails
    global invalid_mails
    invalid_index = 0
    valid_index = 0
    while True:
        invalid_file = open('invalid.txt', 'a')
        for index in range(invalid_index, len(invalid_mails)):
            invalid_file.write(invalid_mails[invalid_index] + "\n")
            invalid_index += 1
        invalid_file.close()
        valid_file = open('valid.txt', 'a')
        for index in range(valid_index, len(valid_mails)):
            valid_file.write(valid_mails[valid_index] + "\n")
            valid_index += 1
        valid_file.close()
        running = False
        for thr in threads:
            if thr.is_alive():
                running = True
                break
        if not running:
            break


emails = []
mail_file = open('emails.txt', 'r')
for email in mail_file:
    emails.append(email.strip())
mail_file.close()
proxy_file = open('proxies.txt', 'r')
proxies = []
for proxy in proxy_file:
    proxies.append(proxy.strip())
proxy_file.close()
in_ = open('invalid.txt', 'w')
in_.write("")
in_.close()
v = open('valid.txt', 'w')
v.write("")
v.close()
no_of_threads = 20
no_of_inputs = math.floor(len(emails) / no_of_threads)
threads = []
option = input("Do you want to use proxy server (y/n) ? ")
for thread in range(no_of_threads):
    start = thread * no_of_inputs
    end = no_of_inputs * (thread + 1)
    if thread == no_of_threads - 1:
        end = len(emails)
    t = threading.Thread(target=validate_emails, name=str(thread), args=(
        start, end,
        proxies[random.randint(0, len(proxies) - 1)]))
    threads.append(t)
    t.start()
threading.Thread(target=write_to_file).start()
