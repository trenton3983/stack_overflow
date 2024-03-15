import requests
import json
import configparser
import time
import logging

# Define constants
BODY_LENGTH_LIMIT = 500
PAGE_SIZE = 100
LOG_LEVEL = logging.INFO
tags = "discussion"

# Set up logging
logging.basicConfig(
    filename=f"./logs/link_only.log", level=LOG_LEVEL
)

# Load the configuration file
config = configparser.ConfigParser()
config.read(r"D:\\users\\trenton\\Dropbox\\PythonProjects\\config_api.ini")

# Get the API key from the configuration file
api_key = config.get("stackapps", "key")

# Define the API endpoint for advanced search
questions_url = "https://api.stackexchange.com/2.3/search/advanced"

# Create a list to store the questions
questions = []

page = 1
while True:
    # Define the parameters for the API request
    params = {
        "order": "desc",
        "sort": "creation",
        "tagged": tags,  # Search for posts with these tags
        "site": "meta.stackoverflow.com",
        "filter": "!-*jbN-o8P3E5",
        "key": api_key,
        "page": page,
        "pagesize": PAGE_SIZE,
        "q": "link only",  # Search for posts with these words in the title
    }

    try:
        # Send the API request
        response = requests.get(questions_url, params=params)
        data = json.loads(response.text)

        # If no items are returned, we've reached the end of the results
        if not data["items"]:
            break

        # For each question, check if the title contains "link only", "link-only", or "linkonly"
        for question in data["items"]:
            title = question["title"].lower()
            if "link only" in title or "link-only" in title or "linkonly" in title:
                # Download the question and its answers
                questions.append(question)

        logging.info(f'Remaining Quota: {data["quota_remaining"]}')
        if "backoff" in data:
            time.sleep(data["backoff"])

        # Increment the page number for the next request
        page += 1

    except requests.exceptions.RequestException as e:
        logging.error(f"Request failed: {e}")
        time.sleep(5)

# New code to download a specific question and its answers
specific_question_url = "https://api.stackexchange.com/2.3/questions/265552/answers"
params = {
    "order": "desc",
    "sort": "activity",
    "site": "meta.stackoverflow.com",
    "filter": "!-*jbN-o8P3E5",
    "key": api_key,
}

try:
    response = requests.get(specific_question_url, params=params)
    data = json.loads(response.text)
    for answer in data["items"]:
        questions.append(answer)
    logging.info(f'Remaining Quota: {data["quota_remaining"]}')
    if "backoff" in data:
        time.sleep(data["backoff"])
except requests.exceptions.RequestException as e:
    logging.error(f"Request failed: {e}")
    time.sleep(5)

# Existing code to save the questions to a file
with open("output/questions.json", "w") as f:
    json.dump(questions, f)

# print the number of questions
print(f"Number of questions: {len(questions)}")
