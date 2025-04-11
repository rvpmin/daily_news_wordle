import json
import random


def find_words_in_article(article):
    words=[]
    for key, values in article.items():
        if type(values) == list:
            for v in values:
                for word in v.split():
                    if len(word) == 5:
                        words.append(word)
        else:
            for word in values.split():
                if len(word) == 5:
                    words.append(word)
    return words

def articles_words(articles):
    articles_data = {}

    for article in articles:
        article = {'title':article['title'], 'abstract':article['abstract'], 'des_facet':article['des_facet'], 'org_facet':article['org_facet'], 'per_facet':article['per_facet'], 'geo_facet':article['geo_facet'], 'url':article['url']}
        words = find_words_in_article(article=article)
        filtered_words = [
            ''.join([c.lower() for c in word if c.isalpha()])
            for word in words
            if len(''.join([c for c in word if c.isalpha()])) == 5
        ]
        articles_data[article['title']] = {
        'words': filtered_words,
        'url': article['url']
        }

    return articles_data

def load_articles():
    with open('nyt_data.json', 'r', encoding='utf-8') as nyt:
        data = json.load(nyt)

    random.seed(42)
    num_articles = 10

    articles = data['results']
    articles = random.sample(articles, k=num_articles)

    return articles

articles = load_articles()
articles_data = articles_words(articles)

with open('nyt_articles_words.json', 'w', encoding='utf-8') as f:
    json.dump(articles_data, f, ensure_ascii=False, indent=4)





        
