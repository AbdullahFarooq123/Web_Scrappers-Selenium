import time

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import json
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.by import By

try:
    chrome_options = Options()
    prefs = {"profile.default_content_setting_values.notifications": 2}
    chrome_options.add_argument('--disable-notifications')
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    chrome_options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get('https://web.whatsapp.com/')
    input('Please login and press enter to continue')
    contacts = []
    i = 500
    pane = driver.find_element(By.CSS_SELECTOR, '#pane-side')
    height = int(pane.get_attribute("scrollHeight"))
    print(height)
    duplicates = []
    while i <= height:
        element = driver.find_element(By.CSS_SELECTOR, '#pane-side > div:nth-child(1) > div > div')
        html = BeautifulSoup(element.get_attribute('innerHTML'), 'html.parser')
        elements = html.findAll('div', {'class': 'lhggkp7q ln8gz9je rx9719la'})
        found = False
        for ele in elements:
            name = ele.find('span',
                            {'class': 'ggj6brxn gfz4du6o r7fjleex g0rxnol2 lhj4utae le5p0ye3 l7jjieqr i0jNr'}).getText()
            # if name not in contacts:
            #     contacts.append(name)
            #     found = True
            duplicates.append(name)
        # print(len(contacts))
        # if not found:
        #     break
        driver.execute_script(f'arguments[0].scrollTop = {i}', pane)
        i += 500
        # time.sleep(1)
    driver.close()
    # d_data = []
    # d_d_data = []
    # # print(len(contacts))
    # print(len(duplicates))
    # for duplicate in duplicates:
    #     found = False
    #     for d in d_data:
    #         if str(duplicate).strip().replace(' ', '') == str(d).strip().replace(' ', ''):
    #             found = True
    #             break
    #     if not found:
    #         d_data.append(duplicate)
    #     else:
    #         d_d_data.append(duplicate)
    # print(len(d_d_data))
    # print(len(d_data))
    # with open('contacts_d.txt', 'w', encoding="utf-8") as file:
    #     for contact in d_d_data:
    #         file.write(contact + '\n')
    with open('contacts.txt', 'w', encoding="utf-8") as file:
        for contact in duplicates:
            file.write(contact + '\n')
except Exception as E:
    print(E)
input('Press enter to close')
