# 📰 Daily News Wordle - Wordle with Real Articles

This project is a Wordle-style guessing game where the player must guess a five-letter word, **extracted from a real New York Times article**. The game updates daily, and each level corresponds to a different article. After each round, the player sees the article's title, abstract, and a link to the original.

## 🧩 Key Features

- 🎯 **Real-word targets**: All target words are sourced from NYT articles (World section).
- 📅 **Daily game**: A new game is generated each day, either automatically or manually from the admin panel.
- 📖 **Multiple levels per game**: Each daily game includes 5 levels, each based on a different article.
- 🧠 **Integrated hints**: After finishing a level, the title, abstract, and original link are revealed.
- 🔐 **Session-based state**: Game progress is saved using `request.session`, with no login required.

## ⚙️ Project Structure

### Core Models

- `Article`: Stores metadata from a NYT article, including the title, abstract, URL, and target word.
- `DailyGame`: Represents the game for a specific day. Contains multiple `GameArticle` entries.
- `GameArticle`: Intermediate model connecting `DailyGame` to specific articles, assigning a level number.
- `WordleGame` and `GameLevel`: More flexible models for manual control through the Wagtail admin interface.

### Main Components

- `utils.py`: Contains functions for:
  - 🔄 Fetching articles from the NYT API.
  - 🧠 Extracting valid 5-letter words.
  - 🎮 Evaluating guesses and handling game logic.
- `views.py`: Contains views for:
  - 🏠 Displaying the homepage and today’s game.
  - ✅ Validating guesses (`check_guess`).
  - 🛠️ Forcing game creation (`force_create_game`).
  - 🧩 Rendering individual game levels.

## 🚀 How It Works

1. **Fetch articles**: Calls the NYT API (`/world.json`) to get the latest articles.
2. **Word extraction**: Extracts five-letter words from article content (title, abstract, etc.).
3. **Game creation**: Builds a `DailyGame` object with selected articles.
4. **Gameplay**:
   - The player sees a level number and enters guesses.
   - Feedback is shown (correct, present, or missing letters).
   - After winning or losing, the original article metadata is displayed.

## 🛠️ Tech Stack

- [Django](https://www.djangoproject.com/)
- [Wagtail CMS](https://wagtail.org/)
- [New York Times Top Stories API](https://developer.nytimes.com/docs/top-stories-product/1/overview)
- JavaScript (for frontend game interaction)
- Django sessions for storing per-user game state

## 📝 Installation


