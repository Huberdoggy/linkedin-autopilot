import os
from time import sleep

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait
from webdriver_manager.firefox import GeckoDriverManager

load_dotenv()


def initiate_driver(url=None, interval=None):
    slp_timeout = interval if interval is not None else None
    driver = webdriver.Firefox(
        service=FirefoxService(GeckoDriverManager().install(), log_path="/dev/null")
    )
    # log_path arg prevents 'gecko.log' in project dir. I don't need it
    navigate_social_media(driver, url, slp_timeout)
    driver.quit()
    driver.stop_client()
    return True


def navigate_social_media(driver, url, interval=None):
    driver.get(f"https://www.{url}")
    driver.maximize_window()
    driver.find_element(By.XPATH, "//input[@id='session_key']").send_keys(
        os.getenv("username")
    )
    driver.find_element(By.XPATH, "//input[@id='session_password']").send_keys(
        os.getenv("password")
    )
    sleep(3)
    driver.find_element(By.XPATH, "//button[@type='submit']").send_keys(Keys.RETURN)
    driver.switch_to.active_element
    # my_network = driver.find_element(By.PARTIAL_LINK_TEXT, "My Network")

    # clickable = WebDriverWait(driver, interval).until(
    #     EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, my_network))
    # )
    # clickable.click()
    if interval is not None:
        sleep(interval)
    return driver
