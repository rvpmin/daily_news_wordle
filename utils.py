from mimetypes import guess_extension

import requests
import os
from django.conf import settings
from django.core.cache import cache
from collections import defaultdict
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

    for article in articles:
        try:
            words = find_words_in_article(article=article)
            filtered_words = [
                ''.join([c.lower() for c in word if c.isalpha()])
                for word in words
                if len(''.join([c for c in word if c.isalpha()])) == 5
            ]
            if not filtered_words:
                filtered_words = ['filth', 'daunt', 'color', 'incur', 'pixie']

            target_word = random.choice(filtered_words)

            processed_date = make_aware(
                datetime.strptime(date, '%Y-%m-%d')
            ) if isinstance(date, str) else date

            processed_article, created = Article.objects.update_or_create(
                url = article['url'],
                defaults = {
                    'title': article['title'],
                    'abstract': article['abstract'],
                    'date_processed': processed_date,
                    'target_word': target_word

                }

            )
            processed.append(processed_article)

            if not created:
                processed_article.title = article['title']
                processed_article.save()


        except Exception as e:
            print(f'Error processing article {article.get["url"]}', e)
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
        self.word_dict = self.create_word_dict(self.word)
        self.guesses = []

    @staticmethod
    def create_word_dict(word):
        word_dict = defaultdict(set)
        for index, letter in enumerate(word):
            word_dict[letter].add(index)
        return word_dict

    def evaluate_guess(self, guess):
        guess = guess.lower()

        guess_result = ['missing' for _ in range(len(self.word))]
        matched_positions = set()

        # Only check correct placements
        for pos in range(len(self.word)):
            if guess[pos] in self.word_dict and pos in self.word_dict[guess[pos]]:
                guess_result[pos] = 'correct'
                matched_positions.add(pos)

        # Check present placements
        for pos in range(len(self.word)):
            if guess_result[pos] == 'missing' and guess[pos] in self.word_dict:
                for correct_pos in self.word_dict[guess[pos]]:
                    if correct_pos not in matched_positions:
                        guess_result[pos] = 'present'
                        matched_positions.add(pos)

        self.guesses.append({'guess': guess, 'result': guess_result})

        if guess == self.word:
            return {'status': 'won', 'guessed': self.guesses}
        elif len(self.guesses) >= self.max_guesses:
            return {'status': 'lost','word':self.word , 'guessed': self.guesses}
        else:
            return {'status': 'continue', 'current_guess':len(self.guesses), 'result':guess_result}

