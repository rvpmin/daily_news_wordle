import requests
import os
from django.conf import settings
from django.core.cache import cache
from collections import defaultdict
import random

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

