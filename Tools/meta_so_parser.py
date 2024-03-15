import requests
import json
import configparser
import time
import logging
import re
from pathlib import Path


class MetaSOParser:
    PAGE_SIZE = 100
    LOG_LEVEL = logging.INFO
    TAGS = "discussion"

    def __init__(self):
        self.current_dir = Path(__file__).parent
        self.config_file_path = self.current_dir / ".." / ".." / "config_api.ini"
        self.config = configparser.ConfigParser()
        self.config.read(self.config_file_path)
        self.api_key = self.config.get("stackapps", "key")
        self.answers = []
        self.links = []
        logging.basicConfig(filename=f"./logs/link_only.log", level=self.LOG_LEVEL)

    def meta_so_link_only(self):
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
            try:
                response = requests.get(questions_url, params=params)
                data = json.loads(response.text)
                if not data["items"]:
                    break
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
                if "backoff" in data:
                    time.sleep(data["backoff"])
                page += 1
            except requests.exceptions.RequestException as e:
                logging.error(f"Request failed: {e}")
                time.sleep(5)
        with open("output/questions.json", "w") as f:
            json.dump(questions, f)
        print(f"Number of questions: {len(questions)}")

    @staticmethod
    def parse_questions_json():
        with open("output/questions.json", "r") as f:
            data = json.load(f)
        with open(
            "output/question_titles.txt", "w", encoding="utf-8"
        ) as titles_file, open(
            "output/question_urls.txt", "w", encoding="utf-8"
        ) as urls_file, open(
            "output/question_body.txt", "w", encoding="utf-8"
        ) as body_file, open(
            "output/answers.txt", "w", encoding="utf-8"
        ) as answers_file:
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

    def download_flagged_link_only_answers(self):
        with open("output/question_urls.txt", "r") as f:
            urls = f.readlines()
        answer_ids = [url.strip().split("/")[-1] for url in urls]
        answers_url = "https://api.stackexchange.com/2.3/answers/{ids}"
        for answer_id in answer_ids:
            params = {
                "order": "desc",
                "sort": "activity",
                "site": "stackoverflow",
                "key": self.api_key,
                "filter": "!-*jbN-o8P3E5",
            }
            answer_details = {
                "answer_id": int(answer_id),
                "is_deleted": True,
                "body": "",
                "link": f"https://stackoverflow.com/a/{answer_id}",
            }
            try:
                response = requests.get(
                    answers_url.format(ids=answer_id), params=params
                )
                data = json.loads(response.text)
                if "items" in data and data["items"]:
                    answer = data["items"][0]
                    answer_details["is_deleted"] = answer.get("is_deleted", False)
                    answer_details["body"] = answer.get("body", "")
                if "backoff" in data:
                    time.sleep(data["backoff"])
            except requests.exceptions.RequestException as e:
                logging.error(f"Request failed: {e}")
                time.sleep(5)
            self.answers.append(answer_details)
        with open("output/flagged_link_only_answers.json", "w") as f:
            json.dump(self.answers, f)


if __name__ == "__main__":
    parser = MetaSOParser()
    parser.meta_so_link_only()
    parser.parse_questions_json()
    parser.download_flagged_link_only_answers()
