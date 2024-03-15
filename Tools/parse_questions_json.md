The `parse_questions_json.py` script is a Python program designed to parse the `questions.json` file, which contains questions and their corresponding answers downloaded from the Stack Exchange API. The script extracts specific information from the JSON data and writes it to separate text files.

Here's a breakdown of what the script does:

1. **Data Loading**: The script begins by loading the `questions.json` file.

2. **File Opening**: The script opens four output files: `question_titles.txt`, `question_urls.txt`, `question_body.txt`, and `answers.txt`. These files will store the extracted question titles, URLs found in the question body, the full question body, and the answers, respectively.

3. **Data Extraction and Writing**: The script iterates over the questions in the JSON data. For each question, it checks if certain keys exist in the question dictionary:

   - If the 'title' key exists, the script writes the title to the `question_titles.txt` file.
   - If the 'body' key exists, the script finds all URLs in the question body and writes them to the `question_urls.txt` file. It also writes the full body text to the `question_body.txt` file.
   - If the 'answers' key exists, the script iterates over the answers. For each answer, it checks if the 'body' key exists and writes the answer body to the `answers.txt` file.

This script is a useful tool for extracting and organizing data from the Stack Exchange API, particularly for questions and answers related to "link only" posts.