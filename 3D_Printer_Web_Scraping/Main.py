import json
import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from Cgtrader import CgTrader
from Minifactory import MiniFactory

with open('pages.json', 'r') as pages_file:
    user_pages = json.load(pages_file)

chrome_options = Options()
prefs = {"profile.default_content_setting_values.notifications": 2}
chrome_options.add_argument('--disable-notifications')
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
chrome_options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
driver.maximize_window()
prev_content_creator_data = {'mini factory': [], 'cgtrader': []}
try:
    with open(os.path.join('prev_data.json'), 'r') as previous_data:
        prev_content_creator_data = json.load(previous_data)
except FileNotFoundError:
    pass

mini_factory = MiniFactory(user_pages=user_pages['mini factory'], driver=driver,
                           prev_content_creator_data=prev_content_creator_data['mini factory'])
mini_factory.get_user_content()
mini_factory.get_image_links()
mini_factory.download_images()

cg_trader = CgTrader(user_pages=user_pages['cgtrader'], driver=driver,
                     prev_content_creator_data=prev_content_creator_data['cgtrader'])
cg_trader.get_user_content()
cg_trader.get_image_data()
cg_trader.download_images()

with open(os.path.join('prev_data.json'), 'w') as previous_data:
    previous_data.write(json.dumps(prev_content_creator_data, indent=4))
    previous_data.close()

driver.close()

print('Script successfully completed!')



