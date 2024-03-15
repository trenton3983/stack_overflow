# README.md

## Stack Overflow Moderation Tools

This directory contains a set of tools developed in Python, specifically designed to assist with the moderation of Stack Overflow.

### Scripts

- [`SO_Linkonly_Parser.py`](SO_Linkonly_Parser.md): This script is used to parse and analyze link-only answers on Stack Overflow. It provides valuable insights and statistics that can be used to improve the quality of answers on the platform.
- [`metaso_linkonly.py`](metaso_linkonly.md): The script is used to find questions on Meta Stack Overflow that are related to link-only answers on Stack Overflow. It also extracts the questions and their respective answers from the website and stores them in a JSON file.
- [`parse_questions_json.py`](parse_questions_json.md): This script is used to parse the JSON data of questions from `metaso_linkonly.py`.
- [`download_flagged_linkonly_answers.py`](download_flagged_linkonly_answers.md): This script is used to download flagged link-only answers from Stack Overflow.

### Contributing

Contributions are welcome. Please feel free to submit a pull request or open an issue if you encounter any problems or have suggestions for improvements.

### License

This project is licensed under the MIT License.