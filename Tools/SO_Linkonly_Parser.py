import requests
import json
from datetime import datetime, timedelta
import configparser
import time
import webbrowser
import logging
from pathlib import Path

# Define constants
DAYS_IN_MONTH = 32
BODY_LENGTH_LIMIT = 500
PAGE_SIZE = 100
LOG_LEVEL = logging.INFO
tags = "python;matplotlib"
start_date = "2024-02-01"
end_date = "2024-02-29"

# Set up logging
logging.basicConfig(
    filename=f"./logs/{start_date}_{end_date}_link_only.log", level=LOG_LEVEL
)


def month_range(start_date, end_date):
    """Generate start and end dates for each month in the range."""
    start_date = start_date.replace(day=1)
    while start_date < end_date:
        end_date_month = (start_date + timedelta(days=DAYS_IN_MONTH)).replace(day=1)
        yield start_date, min(end_date, end_date_month)
        start_date = end_date_month


# Get the current script's directory
current_dir = Path(__file__).parent

# Define the relative path to the config file
config_file_path = current_dir / ".." / "PythonProjects" / "config_api.ini"

# Load the configuration file
config = configparser.ConfigParser()

# Read the config file
config.read(config_file_path)

# Get the API key from the configuration file
api_key = config.get("stackapps", "key")

# Define the API endpoint for questions
questions_url = "https://api.stackexchange.com/2.3/questions"

# Define the start and end dates
start_date = datetime.strptime(start_date, "%Y-%m-%d")
end_date = datetime.strptime(end_date, "%Y-%m-%d")

# Create a list to store the links
links = []

for start_date_month, end_date_month in month_range(start_date, end_date):
    # Convert the dates to Unix timestamp
    start_date_unix = int(start_date_month.timestamp())
    end_date_unix = int(end_date_month.timestamp())

    # Log start_date_str
    logging.info(
        f"Start Date: {start_date_month.strftime('%Y-%m-%d')}, End Date: {end_date_month.strftime('%Y-%m-%d')}"
    )

    page = 1
    while True:
        # Define the parameters for the API request
        params = {
            "order": "desc",
            "sort": "creation",
            "tagged": tags,  # Search for posts with these tags
            "fromdate": start_date_unix,
            "todate": end_date_unix,
            "site": "stackoverflow",
            "filter": "!-*jbN-o8P3E5",
            "key": api_key,
            "page": page,
            "pagesize": PAGE_SIZE,
        }

        try:
            # Send the API request
            response = requests.get(questions_url, params=params)
            data = json.loads(response.text)

            # If no items are returned, we've reached the end of the results
            if not data["items"]:
                break

            # For each question, parse the 'answers' key directly
            for question in data["items"]:
                # Check if the question has answers
                if "answers" in question:
                    # Filter for answers that may primarily be link-only and exclude links from https://i.stack.imgur.com
                    link_only_answers = [
                        item
                        for item in question["answers"]
                        if "http" in item["body"]
                        and "https://i.stack.imgur.com" not in item["body"]
                        and "<code>" not in item["body"]
                        and len(item["body"]) < BODY_LENGTH_LIMIT
                    ]

                    if link_only_answers:
                        logging.info(f"Question ID: {question['question_id']}")
                        # Log the link-only answers
                        for answer in link_only_answers:
                            link = f"https://stackoverflow.com/a/{answer['answer_id']}"
                            logging.info(
                                f"Answer ID: {answer['answer_id']}, Link: {link}"
                            )
                            # Add the link to the list
                            links.append(link)
            logging.info(f'Remaining Quota: {data["quota_remaining"]}')
            if "backoff" in data:
                time.sleep(data["backoff"])

            # Increment the page number for the next request
            page += 1

        except requests.exceptions.RequestException as e:
            logging.error(f"Request failed: {e}")
            time.sleep(5)

# print the number of links
print(f"Number of link-only answers: {len(links)}")

# Open the links in a browser
# for link in links:
#     webbrowser.open(link)
