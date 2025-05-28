import requests
import os
from django.conf import settings
from django.core.cache import cache
from collections import defaultdict, Counter
import random
from .models import Article
from datetime import datetime
from django.utils.timezone import make_aware


def fetch_nyt_api():
    api_key = os.getenv('NYT_API')

    if not api_key:
        raise ValueError('NYT API key not set')
    url = f'https://api.nytimes.com/svc/topstories/v2/world.json?api-key={api_key}'

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data

    except requests.exceptions.RequestException as e:
        print('Error fetching NYT data', e)
        return None


def process_articles(data):
    date = data['last_updated']
    random.seed(0)
    num_articles = 5
    articles = random.sample(data['results'], k=num_articles)
    processed = []
    backup_words = ['filth', 'daunt', 'color', 'incur', 'pixie', 'crane', 'adieu', 'audio', 'house', 'water']

    for article in articles:
        try:
            words = find_words_in_article(article=article)
            filtered_words = [
                ''.join([c.lower() for c in word if c.isalpha()])
                for word in words
                if len(''.join([c for c in word if c.isalpha()])) == 5
            ]
            if not filtered_words:
                filtered_words = backup_words

            target_word = random.choice(filtered_words)

            if isinstance(date, str):
                processed_date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S%z")
            else:
                processed_date = date

            processed_article, created = Article.objects.update_or_create(
                url=article['url'],
                defaults={
                    'title': article['title'],
                    'abstract': article['abstract'],
                    'date_processed': processed_date,
                    'target_word': target_word

                }

            )
            processed.append(processed_article)

        except Exception as e:
            print(f'Error processing article {article.get("url", "unknown")}', {str(e)})
            continue
    return processed


def find_words_in_article(article):
    words = []
    for key, values in article.items():
        if isinstance(values, list):
            for value in values:
                if isinstance(value, str):
                    words.extend(value.split())
        elif isinstance(values, str):
            words.extend(values.split())
    return [word for word in words if len(word) == 5]


class WordleGameEngine:
    def __init__(self, word, max_guesses=6):
        self.word = word.lower()
        self.max_guesses = max_guesses
        self.guesses = []

    def evaluate_guess(self, guess):
        guess = guess.lower()
        result = ['missing'] * len(self.word)

        target = list(self.word)
        guess_letters = list(guess)

        word_counter = Counter(target)

        # Paso 1: marcar letras correctas (posición exacta)
        for i in range(len(guess_letters)):
            if guess_letters[i] == target[i]:
                result[i] = 'correct'
                word_counter[guess_letters[i]] -= 1

        # Paso 2: marcar letras presentes (posición incorrecta)
        for i in range(len(guess_letters)):
            if result[i] == 'missing' and word_counter[guess_letters[i]] > 0:
                result[i] = 'present'
                word_counter[guess_letters[i]] -= 1

        self.guesses.append({'guess': guess, 'result': result})

        if guess == self.word:
            return {'status': 'won', 'guessed': self.guesses}
        elif len(self.guesses) >= self.max_guesses:
            return {'status': 'lost', 'word': self.word, 'guessed': self.guesses}
        else:
            return {
                'status': 'continue',
                'current_guess': len(self.guesses),
                'result': result
            }
