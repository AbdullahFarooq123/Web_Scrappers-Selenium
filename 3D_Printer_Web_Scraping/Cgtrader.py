import json
import os
import time

import requests
from bs4 import BeautifulSoup
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class CgTrader:
    def __init__(self, user_pages, driver, prev_content_creator_data):
        self.user_pages = user_pages
        self.driver = driver
        self.url = 'https://www.cgtrader.com'
        self.prev_content_creator_data = prev_content_creator_data
        self.new_content_creator_data = {}
        self.data_of_image = []
        self.current_directory = os.getcwd()

    def get_user_content(self):
        print('Getting cg trader user content')
        len_of_images = 0
        for page in self.user_pages:
            print(page)
            self.driver.get(page)
            no_of_pages = 0
            author = str(page).split('author=')[1]
            while True:
                try:
                    WebDriverWait(self.driver, 2).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'body')))
                    body = BeautifulSoup(self.driver.find_element(By.CSS_SELECTOR, 'body').get_attribute('innerHTML'),
                                         'html.parser')
                    pages_container = body.find('ul', {'class': 'pagination'})
                    pages_contents = pages_container.find_all('li')
                    last_page = pages_contents[len(pages_contents) - 3]
                    no_of_pages = int(last_page.getText())
                    break
                except AttributeError:
                    pass
            self.new_content_creator_data[author] = []
            for i in range(no_of_pages):
                time_to_sleep = 5
                while True:
                    try:
                        if not i == 0:
                            WebDriverWait(self.driver, 2).until(
                                EC.presence_of_element_located((By.CSS_SELECTOR, 'body')))
                            body = BeautifulSoup(
                                self.driver.find_element(By.CSS_SELECTOR, 'body').get_attribute('innerHTML'),
                                'html.parser')
                            pages_container = body.find('ul', {'class': 'pagination'})
                            pages_contents = pages_container.find_all('li')
                            next_page = self.url + pages_contents[len(pages_contents) - 2].find('a').get('href')
                            self.driver.get(next_page)
                            time.sleep(time_to_sleep)
                        WebDriverWait(self.driver, 2).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'body')))
                        body = BeautifulSoup(
                            self.driver.find_element(By.CSS_SELECTOR, 'body').get_attribute('innerHTML'),
                            'html.parser')
                        parent_container = body.find('div', {'class': 'content-box-wrapper'})
                        child_containers = parent_container.find_all('div', {
                            'class': 'js-fast-listing-item content-box content-box--interactive previewable'})
                        for container in child_containers:
                            link = container.find('a', {'class': 'content-box__link js-track-click'}).get('href')
                            if link not in self.prev_content_creator_data:
                                self.prev_content_creator_data.append(link)
                                self.new_content_creator_data[author].append(link)
                                len_of_images+=1
                        break
                    except AttributeError:
                        time_to_sleep += 1
        print('Got cg trader content, New Content found : ' + str(len_of_images))

    def get_image_data(self):
        print('Getting images links of users')
        time_to_sleep = 0
        for author in self.new_content_creator_data:
            for image in self.new_content_creator_data[author]:
                while True:
                    try:
                        self.driver.get(image)
                        time.sleep(time_to_sleep)
                        WebDriverWait(self.driver, 2).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'body')))
                        body = BeautifulSoup(
                            self.driver.find_element(By.CSS_SELECTOR, 'body').get_attribute('innerHTML'),
                            'html.parser')
                        title = body.find('h1', {'class': 'product-header__title'}).getText()
                        try:
                            price = body.find('strong', {'class': 'main-price'}).getText()
                            image_link = body.find('div', {'class': 'product-carousel__image'}).find(
                                'img').get('src')
                            self.data_of_image.append({
                                'title': title,
                                'price': price,
                                'link': image_link,
                                'author': author,
                            })
                        except AttributeError:
                            pass
                        time_to_sleep -= 1
                        if time_to_sleep < 0:
                            time_to_sleep = 0
                        break
                    except (AttributeError, TimeoutException):
                        time_to_sleep += 1
        print('Got images links')

    def download_images(self):
        print('Downloading Images')
        for image_link in self.data_of_image:
            img_url = image_link['link']
            img_name = image_link['title'].replace('\n', '').replace('\t', '').replace('\\', '').replace('/',
                                                                                                         '').replace(
                ':',
                '').replace(
                '*', '').replace('*', '').replace('?', '').replace('"', '').replace('<', '').replace('>', '').replace(
                '|',
                '').strip()
            price = image_link['price']
            path = image_link['author']
            try:
                os.mkdir(path)
            except FileExistsError:
                pass
            file_name = os.path.join(os.path.join(self.current_directory, path), img_name + '.png')
            response = requests.get(img_url)
            if response.status_code:
                fp = open(file_name, 'wb')
                fp.write(response.content)
                fp.close()
        print('Images Downloaded')
