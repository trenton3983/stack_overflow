import requests
import json
import configparser
import time
import logging
import re
from pathlib import Path

# Define a class for parsing Meta StackOverflow
class MetaSOParser:
    # Define constants for the class
    PAGE_SIZE = 100
    LOG_LEVEL = logging.INFO
    TAGS = "discussion"

    # Initialize the parser
    def __init__(self):
        # Set up paths and configuration
        self.current_dir = Path(__file__).parent
        self.config_file_path = self.current_dir / ".." / ".." / "config_api.ini"
        self.config = configparser.ConfigParser()
        self.config.read(self.config_file_path)
        self.api_key = self.config.get("stackapps", "key")
        self.answers = []
        self.links = []
        # Set up logging
        logging.basicConfig(filename=f"./logs/link_only.log", level=self.LOG_LEVEL)

    # Define a method for making API requests
    def api_request(self, url, params):
        # Try to make the request and handle exceptions
        try:
            response = requests.get(url, params=params)
            data = json.loads(response.text)
            if "backoff" in data:
                time.sleep(data["backoff"])
            return data
        except requests.exceptions.RequestException as e:
            logging.error(f"Request failed: {e}")
            time.sleep(5)
            return None

    # Define a method for getting link-only posts from Meta SO
    def meta_so_link_only(self):
        # Set up the API endpoint and parameters
        questions_url = "https://api.stackexchange.com/2.3/search/advanced"
        questions = []
        page = 1
        while True:
            params = {
                "order": "desc",
                "sort": "creation",
                "tagged": self.TAGS,
                "site": "meta.stackoverflow.com",
                "filter": "!-*jbN-o8P3E5",
                "key": self.api_key,
                "page": page,
                "pagesize": self.PAGE_SIZE,
                "q": "link only",
            }
            # Make the API request
            data = self.api_request(questions_url, params)
            if not data or not data["items"]:
                break
            # Filter the questions and add them to the list
            questions.extend(
                [
                    question
                    for question in data["items"]
                    if any(
                        x in question["title"].lower()
                        for x in ["link only", "link-only"]
                    )
                ]
            )
            page += 1
        # Write the questions to a file
        with open("output/questions.json", "w") as f:
            json.dump(questions, f)
        print(f"Number of questions: {len(questions)}")

    # Define a method for parsing the questions JSON
    @staticmethod
    def parse_questions_json():
        # Open the questions file and read the data
        with open("output/questions.json", "r") as f:
            data = json.load(f)
        # Open output files for writing
        with open(
            "output/question_titles.txt", "w", encoding="utf-8"
        ) as titles_file, open(
            "output/question_urls.txt", "w", encoding="utf-8"
        ) as urls_file, open(
            "output/question_body.txt", "w", encoding="utf-8"
        ) as body_file, open(
            "output/answers.txt", "w", encoding="utf-8"
        ) as answers_file:
            # Loop through the questions and write data to the files
            for question in data:
                titles_file.write(question.get("title", "") + "\n")
                urls = re.findall(
                    r"https?://stackoverflow.com/a/\d+", question.get("body", "")
                )
                for url in urls:
                    urls_file.write(url + "\n")
                body_file.write(question.get("body", "") + "\n")
                for answer in question.get("answers", []):
                    answers_file.write(
                        f"Score: {answer.get('score', '')} - {answer.get('body', '')}\n"
                    )

    # Define a method for downloading flagged link-only answers
    def download_flagged_link_only_answers(self):
        # Open the URLs file and read the data
        with open("output/question_urls.txt", "r") as f:
            urls = f.readlines()
        # Extract the answer IDs from the URLs
        answer_ids = [url.strip().split("/")[-1] for url in urls]
        # Set up the API endpoint
        answers_url = "https://api.stackexchange.com/2.3/answers/{ids}"
        # Loop through the answer IDs and make API requests
        for answer_id in answer_ids:
            params = {
                "order": "desc",
                "sort": "activity",
                "site": "stackoverflow",
                "key": self.api_key,
                "filter": "!-*jbN-o8P3E5",
            }
            # Set up a dictionary for the answer details
            answer_details = {
                "answer_id": int(answer_id),
                "is_deleted": True,
                "body": "",
                "link": f"https://stackoverflow.com/a/{answer_id}",
            }
            # Make the API request
            data = self.api_request(answers_url.format(ids=answer_id), params)
            if data and "items" in data and data["items"]:
                answer = data["items"][0]
                answer_details["is_deleted"] = answer.get("is_deleted", False)
                answer_details["body"] = answer.get("body", "")
            # Add the answer details to the list
            self.answers.append(answer_details)
        # Write the answers to a file
        with open("output/flagged_link_only_answers.json", "w") as f:
            json.dump(self.answers, f)


# Main execution
if __name__ == "__main__":
    # Create a parser and run the methods
    parser = MetaSOParser()
    parser.meta_so_link_only()
    parser.parse_questions_json()
    parser.download_flagged_link_only_answers()