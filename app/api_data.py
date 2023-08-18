import os
import re
from time import sleep

from dotenv import load_dotenv

load_dotenv()
from linkedin_api import Linkedin


def connect_api(interval=None, **data):
    # We need to resolve some imports if module is run directly
    # from cmd line, instead of 'main_menu'
    if data:
        for value in data.values():
            f"import {value}"
            print(f"Imported {value}.py")
    print("Please wait while we scrape data from LinkedIn...\n\n")
    api = Linkedin(os.getenv("username"), os.getenv("password"))

    try:
        job_lst = api.search_jobs(
            keywords="software developer",
            experience=["2", "3"],
            job_type=["F", "C"],
            remote=True,
            listed_at=86_400,  # corresponds to 24 hrs (3600 secs * 24)
            limit=5,
        )
        print("Found new jobs!\n\n")
        for i in range(len(job_lst)):
            title = job_lst[i]["title"]
            location = job_lst[i]["formattedLocation"]
            job_match = re.search(
                r"\bfs[_d](_normalized)?_jobPosting:(\d+)\b", str(job_lst[i])
            )
            job_id = job_match.group(2)
            parsed = api.get_job(job_id=job_id)
            print(
                f"Company: {parsed['companyDetails']['com.linkedin.voyager.deco.jobs.web.shared.WebCompactJobPostingCompany']['companyResolutionResult']['name']}\n"
            )
            print(f"Title: {title}\nLocation: {location}\n")
            print(f"Job Info:\n\n{parsed['description']['text']}")

            # for k, v in parsed.items():
            #     print(f"Key is: {k}\nValue is {v}")
            print("*" * 50 + "\n")
        if interval:
            sleep(interval)  # Workaround so if run from 'main_menu.py',
        # we can avoid extra import complexities and just pass it
        # a delay to read the results prior to function return
    except KeyError:
        print("Invalid data request.")
        sleep(3)
    return True


if __name__ == "__main__":  # For testing in isolation mostly
    print("Running send_invites.py directly...\n")
    connect_api(support_file1="support", support_file2="common")
