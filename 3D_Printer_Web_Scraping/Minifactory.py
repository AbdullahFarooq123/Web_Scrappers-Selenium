import os
import time

import requests
from bs4 import BeautifulSoup
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import static


class MiniFactory:
    def __init__(self, user_pages, driver, prev_content_creator_data):
        self.user_pages = user_pages
        self.driver = driver
        self.url = 'https://www.myminifactory.com'
        self.prev_content_creator_data = prev_content_creator_data
        self.new_content_creator_data = {}
        self.data_of_image = []
        self.current_directory = os.getcwd()
        self.error_limit = 5

    def get_user_content(self):
        print('Getting minifactory user data')
        for page in self.user_pages:
            self.driver.get(page)
            error = 0
            while error <= self.error_limit:
                try:
                    WebDriverWait(self.driver, 2).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'body')))
                    body = BeautifulSoup(self.driver.find_element(By.CSS_SELECTOR, 'body').get_attribute('innerHTML'),
                                         'html.parser')
                    nav_bottom = body.find('nav')
                    pages_container = nav_bottom.find('ul')
                    pages = pages_container.find_all('li')
                    break
                except AttributeError:
                    error += 1
                    pass
            static.validate_error(error=error, limit=self.error_limit)
            author = str(page).split('https://www.myminifactory.com/users/')[1].split('?')[0]
            self.new_content_creator_data[author] = []
            len_of_images = 0
            for i in range(len(pages) - 1):
                time_to_sleep = 5
                error = 0
                while error <= self.error_limit:
                    try:
                        if not i == 0:
                            this_page = self.url + pages[i].find('a').get('href')
                            self.driver.get(this_page)
                            time.sleep(time_to_sleep)
                        WebDriverWait(self.driver, 2).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'body')))
                        body = BeautifulSoup(
                            self.driver.find_element(By.CSS_SELECTOR, 'body').get_attribute('innerHTML'),
                            'html.parser')
                        parent_container = body.find('div', {'class': 'jss92'})
                        child_containers = parent_container.find_all('div', {'class': 'jss91'})
                        for container in child_containers:
                            link = container.find('a').get('href')
                            if link not in self.prev_content_creator_data:
                                self.prev_content_creator_data.append(link)
                                self.new_content_creator_data[author].append(link)
                                len_of_images+=1
                        break
                    except AttributeError:
                        error += 1
                        time_to_sleep += 1
                static.validate_error(error=error, limit=self.error_limit)
        print('Got user data, Found new images : ' + str(len_of_images))

    def get_image_links(self):
        print('Getting images links of users')
        time_to_sleep = 0
        for author in self.new_content_creator_data:
            for image in self.new_content_creator_data[author]:
                error = 0
                while error <= self.error_limit:
                    try:
                        self.driver.get(image)
                        time.sleep(time_to_sleep)
                        WebDriverWait(self.driver, 2).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'body')))
                        body = BeautifulSoup(
                            self.driver.find_element(By.CSS_SELECTOR, 'body').get_attribute('innerHTML'),
                            'html.parser')
                        title = body.find('h1', {'class': 'obj-title'}).getText()
                        try:
                            price = body.find('span', {'class': 'price-title'}).getText()
                            image_link = body.find('div', {'class': 'slick-slide slick-active slick-center'}).find(
                                'img').get('src')
                            self.data_of_image.append({
                                'title': title,
                                'price': price,
                                'link': image_link,
                                'author': author
                            })
                        except AttributeError:
                            pass
                        time_to_sleep -= 1
                        if time_to_sleep < 0:
                            time_to_sleep = 0
                        break
                    except (AttributeError, TimeoutException):
                        error += 1
                        time_to_sleep += 1
                    static.validate_error(error=error, limit=self.error_limit)
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
            author = image_link['author']
            path = author + '\\' + self.price_compare(price)
            try:
                os.mkdir(author)
            except FileExistsError:
                pass
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

    def price_compare(self, price_to_comp: str):
        price_value = float(price_to_comp.replace('$', ''))
        if price_value <= 5:
            return 'low'
        elif 5.1 <= price_value <= 8:
            return 'medium'
        elif 8.1 <= price_value <= 10:
            return 'mhigh'
        elif 10.1 <= price_value <= 12:
            return 'high'
        else:
            return 'very high'
