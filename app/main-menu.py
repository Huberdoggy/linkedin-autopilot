import os
import re
import sys

from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from support import add_to_path
from webdriver_manager.firefox import GeckoDriverManager

# Needed before I can access my external imports from common.py below...
add_to_path()
from common import (
    compile_patterns,
    format_main_menu,
    make_menu,
    print_green,
    print_red,
    screen_clear,
)
from send_invites import test_raise
from send_messages import navigate_social_media
from support import people_dict, xpath_dict


def initiate_driver(url=None, interval=None):
    slp_timeout = interval if interval is not None else None
    driver = webdriver.Firefox(
        service=FirefoxService(GeckoDriverManager().install(), log_output="/dev/null")
    )
    # log_path arg prevents 'gecko.log' in project dir. I don't need it
    navigate_social_media(driver, url, slp_timeout, xpaths=xpath_dict, people=people_dict)
    driver.quit()
    return True


def determine_module(choice):
    if choice == 1:  # Todo
        screen_clear()
        try:
            module = test_raise()
        except Exception as e:
            module = f"AN ERROR OCCURRED: {e.args[1]}"
            print(module)
            screen_clear(5)
    elif choice == 2:
        screen_clear()
        module = initiate_driver(url="linkedin.com", interval=5)
    else:
        return  # Exit prog - chose 3
    return module


reg_patterns = {
    "menu_sel_pattern": "^[1-3]{1}$",
}

compile_patterns(reg_patterns)
welcome_str = "LinkedIn Auto-Pilot"
opts_lst = [
    f"Search people & send invites to grow {os.getenv('USER').capitalize()}'s network",
    f"Send messages to {os.getenv('USER').capitalize()}'s connections",
    "Quit",
]
main_menu_dict = make_menu(opts_lst[0], opts_lst[1], opts_lst[2])
valid_input = False
while not valid_input:
    screen_clear()
    format_main_menu(welcome_str, main_menu_dict)
    choice = input("=> ").strip()
    if re.fullmatch(reg_patterns.get("menu_sel_pattern", "Non Existent"), choice):
        keep_running = determine_module(int(choice))
        if keep_running is None:
            screen_clear()
            print_green("Thankyou. Good bye!")
            sys.exit(0)
    else:
        screen_clear()
        print_red(
            "Invalid input\nPlease enter a number correspoding to one of the \
given options."
        )
        screen_clear(2)
