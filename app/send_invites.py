import os
import subprocess

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
from selenium.webdriver.support.ui import WebDriverWait
from support import people_dict, xpath_dict
from webdriver_manager.firefox import GeckoDriverManager

load_dotenv()


def initiate_driver(url=None, interval=None):
    slp_timeout = interval if interval is not None else None
    driver = webdriver.Firefox(
        service=FirefoxService(GeckoDriverManager().install(), log_path="/dev/null")
    )
    # log_path arg prevents 'gecko.log' in project dir. I don't need it
    navigate_social_media(driver, url, slp_timeout, xpaths=xpath_dict, people=people_dict)
    driver.quit()
    return True


def get_os_monitors():
    cmd = r"xrandr --listactivemonitors | grep -Eoi '\bmonitors:\s[1-2]{1}\b' | awk -F: '{print $2}'"

    xrandr_ps = subprocess.Popen(
        cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    )

    try:
        output = xrandr_ps.communicate()[0].decode("utf-8").strip()
        output = int(output)
        return output
    except Exception as e:
        print(e)


def check_for_captcha(driver):
    xpath = '//h1[text()="Let\'s do a quick security check"]'
    try:
        driver.find_element(By.XPATH, xpath)
        return driver
    except Exception:  # No captcha. Delay not needed
        return None


def navigate_social_media(driver, url, interval=None, **data):
    creds = dict(islice(data["xpaths"].items(), None, 3, None))
    cmds = dict(islice(data["xpaths"].items(), 3, len(xpath_dict), None))
    # returns iterator in their default ordering - uses start, stop, step
    x_coord = 2000 if get_os_monitors() > 1 else 0
    print(f"X coordinate is: {x_coord}")
    driver.set_window_position(x_coord, 0)  # When using single monitor, remove this
    # Set window mid built-in screen (right). Leave big monitor open for output/code
    driver.maximize_window()
    driver.delete_all_cookies()
    driver.set_page_load_timeout(
        (interval + 20) if interval is not None else 25
    )  # defaults to 5, passed from main_menu
    web_wait_timeout = 10
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

        if check_for_captcha(driver) is not None:
            print("Extending delay to account for security check...")
            sleep((interval + 20) if interval is not None else 25)

        driver.switch_to.active_element
        for key in cmds:
            if key == "name_search_box":
                clickable = WebDriverWait(driver, web_wait_timeout).until(
                    EC.element_to_be_clickable((By.XPATH, f"{cmds[key]}"))
                )
                clickable.send_keys(data["people"]["brother"].get("name"))
                driver.switch_to.default_content
                sleep(interval if interval is not None else 5)
            elif key == "write_msg_box":
                clickable = WebDriverWait(driver, web_wait_timeout).until(
                    EC.element_to_be_clickable((By.XPATH, f"{cmds[key]}"))
                )
                clickable.send_keys(data["people"]["brother"].get("message"))
            else:
                clickable = WebDriverWait(driver, web_wait_timeout).until(
                    EC.element_to_be_clickable((By.XPATH, f"{cmds[key]}"))
                )
                clickable.click()
        sleep(interval if interval is not None else 5)
    except selenium.common.exceptions.NoSuchElementException as e:
        print(f"Error caught:\n\n{e.msg}")
        sleep(interval if interval is not None else 5)
    finally:
        return driver
