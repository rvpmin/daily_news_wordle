import json
import wordle
import random

random.seed(42)
with open('nyt_articles_words.json', 'r', encoding='utf-8') as nyt:
        data = json.load(nyt)
score = 0
i = 0
for title, info in data.items(): 
        i += 1
        with open("wordle_article_words.txt", "w") as file:
            file.write(' '.join(info['words']))
        print(f'Game {i}')
        s = wordle.main('wordle_article_words.txt')
        score += s
        print(f'The article this word was from is: {title}')
        print(f'Read it at: {info['url']}\n')
        if i < 5:
            play_again = input('Do you want to play again? (y/n)  ')
            print('\n')
            if play_again == 'y':
                continue
            else:
                print('Thank you for playing!')
                break
        elif i == 5:
            print("That's all for now, thank you for playing!")
            break
print(f'Your score was: {score}/5')
                