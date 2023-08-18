import os
import re
import sys

import support

# Needed before I can access my external imports from common.py below...
support.add_to_path()
import api_data
import common
import send_invites


def determine_module(choice):
    if choice == 1:
        common.screen_clear()
        module = api_data.connect_api(interval=10)
    elif choice == 2:
        common.screen_clear()
        module = send_invites.initiate_driver(url="linkedin.com", interval=5)
    else:
        return  # Exit prog - chose 3
    return module


reg_patterns = {
    "menu_sel_pattern": "^[1-3]{1}$",
}

common.compile_patterns(reg_patterns)
welcome_str = "LinkedIn Auto-Pilot"
opts_lst = [
    f"Shortlist jobs with {os.getenv('USER').capitalize()}'s keywords",
    "Search/send invites to 2nd connections",
    "Quit",
]
main_menu_dict = common.make_menu(opts_lst[0], opts_lst[1], opts_lst[2])
valid_input = False
while not valid_input:
    common.screen_clear()
    common.format_main_menu(welcome_str, main_menu_dict)
    choice = input("=> ").strip()
    if re.fullmatch(reg_patterns.get("menu_sel_pattern", "Non Existent"), choice):
        keep_running = determine_module(int(choice))
        if keep_running is None:
            common.screen_clear()
            common.print_green("Thankyou. Good bye!")
            sys.exit(0)
    else:
        common.screen_clear()
        common.print_red(
            "Invalid input\nPlease enter a number correspoding to one of the \
given options."
        )
        common.screen_clear(2)
