# Discord Quiz Bot

This is a bot that asks users trivia questions and keeps track of their scores. The questions are loaded from a `questions.json` file, and user data is stored in a `user_data.json` file. This bot was possibly made for CTF (Capture The Flag) stuff in the future.

## Installation

1. Clone this repository: `git clone https://github.com/AIMadeScripts/discordbotquiz.git`
2. Install the required dependencies: `pip install -r requirements.txt`
3. Run the bot: `python questions.py`

## Usage

The bot has several commands:

- `!ask` - asks the user a new question
- `!answer <user_answer>` - checks the user's answer and updates their score
- `!current` - tells the user their current question
- `!points` - tells the user their current score
- `!reset` - resets the user's score and progress
- `!leaderboard` - displays the current leaderboard

## Contributing

If you'd like to contribute to this project, feel free to submit a pull request. Please make sure to follow the existing code style and include tests for any new functionality.

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).
