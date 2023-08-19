import os

# import sys
from itertools import islice
from time import sleep

import selenium.common.exceptions
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait
from support import xpath_dict
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
    creds = dict(islice(xpath_dict.items(), None, 3, None))
    cmds = dict(islice(xpath_dict.items(), 3, len(xpath_dict), None))
    # returns iterator in their default ordering - uses start, stop, step
    driver.maximize_window()
    driver.delete_all_cookies()
    driver.set_page_load_timeout((interval + 20) if interval is not None else 25)
    driver.implicitly_wait((interval + 5) if interval is not None else 10)
    driver.get(f"https://www.{url}")
    driver.refresh()  # In the event it hangs

    try:
        for key in creds:
            if key == "form_field_u":
                driver.find_element(By.XPATH, f"{creds[key]}").send_keys(
                    os.getenv("username")
                )
            elif key == "form_field_p":
                driver.find_element(By.XPATH, f"{creds[key]}").send_keys(
                    os.getenv("password")
                )
            else:
                driver.find_element(By.XPATH, f"{creds[key]}").send_keys(Keys.RETURN)
        two_factor = driver.find_element(
            By.XPATH,
            '//h1[text()="Let\'s do a quick security check"]',
        )
        if two_factor:
            print("Extending delay to account for security check...")
            sleep(25)
        driver.switch_to.active_element

        for key in cmds:
            if key == "name_search_box":
                clickable = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, f"{cmds[key]}"))
                )
                clickable.send_keys("Stephen Huber")
                driver.switch_to.default_content
                sleep(5)
            elif key == "write_msg_box":
                clickable = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, f"{cmds[key]}"))
                )
                clickable.send_keys("Hey bro. This is an automated message from Python.")
                clickable.send_keys(Keys.RETURN)
            else:
                clickable = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, f"{cmds[key]}"))
                )
                clickable.click()
        sleep(interval) if interval is not None else 5
    except (
        selenium.common.exceptions.NoSuchElementException
        or selenium.common.exceptions.ElementNotInteractableError
    ) as e:
        print(e.msg)
    return driver


# if __name__ == "__main__":
#     initiate_driver()
