import os
from time import sleep

from dotenv import load_dotenv
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
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
    return True


def navigate_social_media(driver, url, interval=None):
    driver.maximize_window()
    driver.delete_all_cookies()
    driver.set_page_load_timeout((interval + 20) if interval is not None else 25)
    driver.implicitly_wait((interval + 5) if interval is not None else 10)
    driver.get(f"https://www.{url}")
    driver.refresh()  # In the event it hangs
    try:
        driver.find_element(By.XPATH, "//input[@id='session_key']").send_keys(
            os.getenv("username")
        )
        driver.find_element(By.XPATH, "//input[@id='session_password']").send_keys(
            os.getenv("password")
        )
        driver.find_element(By.XPATH, "//button[@type='submit']").send_keys(Keys.RETURN)
        driver.switch_to.active_element
        clickable = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[@title='My Network']"))
        )
        clickable.click()
        clickable = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//a[starts-with(@id, 'ember')]//div//div[text()='Connections']",
                )
            )
        )
        clickable.click()
        clickable = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//input[@type='search' and @placeholder='Search by name']",
                )
            )
        )
        clickable.send_keys("<Name from contacts>")
        clickable = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//button[starts-with(@aria-label, 'Send a message')]",
                )
            )
        )
        clickable.click()
        clickable = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//*[@data-placeholder='Write a message...']",
                )
            )
        )
        clickable.send_keys("<Dummy message>")
        if interval is not None:
            sleep(interval)
    except NoSuchElementException as e:
        print(e.msg)
    return driver
