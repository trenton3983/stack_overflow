import json
import re

# Load the JSON data
with open("output/questions.json", "r") as f:
    data = json.load(f)

# Open the output files
with (open("output/question_titles.txt", "w", encoding="utf-8") as titles_file,
      open("output/question_urls.txt", "w", encoding="utf-8") as urls_file,
      open("output/question_body.txt", "w", encoding="utf-8") as body_file,
      open("output/answers.txt", "w", encoding="utf-8") as answers_file):

    # Iterate over the questions
    for question in data:
        # Check if the 'title' key exists
        if "title" in question:
            # Write the title to the titles_file
            titles_file.write(question["title"] + "\n")

        # Check if the 'body' key exists
        if "body" in question:
            # Find all URLs in the question body
            urls = re.findall(r"https?://stackoverflow.com/a/\d+", question["body"])

            # Write the URLs to the question_urls.txt file
            for url in urls:
                urls_file.write(url + "\n")

            # Write the full body text to the question_body.txt file
            body_file.write(question["body"] + "\n")

        # Check if the 'answers' key exists
        if "answers" in question:
            # Iterate over the answers
            for answer in question["answers"]:
                # Check if the 'body' key exists in the answer
                if "body" in answer:
                    # Check if the 'score' key exists in the answer
                    if "score" in answer:
                        # Write the answer score and body to the answers_file
                        answers_file.write(
                            f"Score: {answer['score']} - {answer['body']}\n"
                        )
                    else:
                        # Write the answer body to the answers_file
                        answers_file.write(answer["body"] + "\n")
