import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import logging
import traceback


class GetPages:
    def __init__(self, driver: WebDriver, url: str):
        self.driver = driver
        self.driver.get(url)
        self.no_of_followers = 0

    def get_num_followers(self, wait):
        while True:
            try:
                follower_btn = WebDriverWait(self.driver, wait).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'body')))
                html = BeautifulSoup(follower_btn.get_attribute('innerHTML'), 'html.parser')
                followers = html.find_all('span', {'class': '_ac2a'})
                if len(followers) == 0:
                    return [False, False]
                self.no_of_followers = int(followers[1].getText().replace(',', ''))
                if 'K' in followers[1].getText().upper():
                    self.no_of_followers = float(followers[1].getText()[:-1]) * 10 ** 3
                elif 'M' in followers[1].getText().upper():
                    self.no_of_followers = float(followers[1].getText()[:-1]) * 10 ** 6
                return [True, False]
            except TimeoutException:
                print('Network Error')
                return [False, True]


def get_followers(self):
    follower_btn = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                                                        'body > div > div > div:nth-child(1) > div > div:nth-child(3) > div > div > div:nth-child(1) > div:nth-child(1) > section > main > div > header > section > ul > li:nth-child(2) > a')))
    follower_btn.click()
    followers = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                                                     'body > div > div > div:nth-child(1) > div > div:nth-child(4) > div > div > div.rq0escxv.l9j0dhe7.du4w35lb > div > div.iqfcb0g7.tojvnm2t.a6sixzi8.k5wvi7nf.q3lfd5jv.pk4s997a.bipmatt0.cebpdrjk.qowsmv63.owwhemhu.dp1hu0rb.dhp61c6y.l9j0dhe7.iyyx5f41.a8s20v7p > div > div > div > div > div > div > div > div._aano')))
    self.driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', followers)
    self.driver.close()


def get_post_link(self):
    posts = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                                                 'body > div > div > div:nth-child(1) > div > div.rq0escxv.l9j0dhe7.du4w35lb > div > div > div.j83agx80.cbu4d94t.d6urw2fd.dp1hu0rb.l9j0dhe7.du4w35lb > div._a3gq > section > main > div > div._aa-i > article > div:nth-child(1) > div')))
    html = BeautifulSoup(posts.get_attribute('innerHTML'), 'html.parser')
    divs = html.find_all('div._ac7v._aang')
    for div in divs:
        print(div)
    # total_posts = 0
    # print(len(divs))
    # for i in range(len(divs)):
    #     post = self.driver.find_element(By.CSS_SELECTOR, 'body > div > div > div:nth-child(1) > div > div.rq0escxv.l9j0dhe7.du4w35lb > div > div > div.j83agx80.cbu4d94t.d6urw2fd.dp1hu0rb.l9j0dhe7.du4w35lb > div._a3gq > section > main > div > div._aa-i > article > div:nth-child(1) > div > div' )
    #     html_2 = BeautifulSoup(post.get_attribute('innerHTML'), 'html.parser')
    #     divs_2 = html_2.findAll('div')
    #     total_posts += len(divs_2)
    # print(total_posts)
