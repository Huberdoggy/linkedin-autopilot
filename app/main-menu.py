import os
import re
import sys

from support import add_to_path

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
from send_invites import initiate_driver


def determine_module(choice):
    if choice == 1:
        screen_clear()
        module = initiate_driver(url="linkedin.com", interval=5)
    elif choice == 2:  # Todo
        screen_clear()
        raise NotImplementedError
    else:
        return  # Exit prog - chose 3
    return module


reg_patterns = {
    "menu_sel_pattern": "^[1-3]{1}$",
}

compile_patterns(reg_patterns)
welcome_str = "LinkedIn Auto-Pilot"
opts_lst = [
    "Search/send invites to 2nd connections",
    f"{os.getenv('USER').capitalize()} will implement future functionality",
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
