"""
Environment for Behave Testing
"""
from os import getenv
from selenium import webdriver
import logging

logging.basicConfig(level=logging.INFO)

WAIT_SECONDS = int(getenv('WAIT_SECONDS','60'))
BASE_URL = getenv('BASE_URL','http://localhost:8080')

def before_all(context):
    """ Executed once before all tests """
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox") #bypass OS securirt model
    options.add_argument("--disable-dev-shm-usage")
    context.driver = webdriver.Chrome(options=options)
    context.wait_seconds = WAIT_SECONDS
    context.driver.implicitly_wait(context.wait_seconds) #seconds
    context.base_url = BASE_URL
    logging.info("Browser started at: %s", context.base_url)
def after_all(context):
    """ Executed after all tests """
    context.driver.quit()
    logging.info("Browser closed.")