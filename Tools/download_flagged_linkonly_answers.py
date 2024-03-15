import requests
import json
import configparser
import time
import logging
from pathlib import Path

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

# Read the question_urls.txt file and extract the answer IDs
with open("output/question_urls.txt", "r") as f:
    urls = f.readlines()
answer_ids = [url.strip().split("/")[-1] for url in urls]

# Define the API endpoint for answers
answers_url = "https://api.stackexchange.com/2.3/answers/{ids}"

# Create a list to store the answers
answers = []

for answer_id in answer_ids:
    # Define the parameters for the API request
    params = {
        "order": "desc",
        "sort": "activity",
        "site": "stackoverflow",
        "key": api_key,
        "filter": "!-*jbN-o8P3E5",
    }

    # Initialize the answer_details dictionary with default values
    answer_details = {
        "answer_id": int(answer_id),
        "is_deleted": True,
        "body": "",
        "link": f"https://stackoverflow.com/a/{answer_id}"
    }

    try:
        # Send the API request
        response = requests.get(answers_url.format(ids=answer_id), params=params)
        data = json.loads(response.text)

        # If the 'items' key is in the data, update the answer_details dictionary
        if "items" in data and data["items"]:
            answer = data["items"][0]
            answer_details["is_deleted"] = answer.get("is_deleted", False)
            answer_details["body"] = answer.get("body", "")

        if "backoff" in data:
            time.sleep(data["backoff"])

    except requests.exceptions.RequestException as e:
        logging.error(f"Request failed: {e}")
        time.sleep(5)

    # Append the answer_details dictionary to the answers list
    answers.append(answer_details)

# Write the answers to a JSON file
with open("output/flagged_linkonly_answers.json", "w") as f:
    json.dump(answers, f)
