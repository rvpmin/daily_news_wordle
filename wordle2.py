import random
import string
from collections import defaultdict


def get_word(f):
    words = f.read().split()
    word = random.choice(words).lower()
    word_dict = defaultdict(set)
    for index, letter in enumerate(word):
        word_dict[letter].add(index)
    return word_dict, word


def language_select():
    if LANGUAGE == 'español':
        palabra = 'Intento'
        f = open(WORDS_PATH + WORDS_ESP, "r")
        text = (f'Bienvenido a Wordle, intenta aadivinar la palabar en {NUM_GUESSES} intentos\n'
                f'Instrucciones\n'
                f'+Cada intento debe ser una palabra de {NUM_LETTERS} letras\n'
                f'+Para cada letra, si tiene debajo un "o", la letra se encuentra en la palabra y está bien colocada\n'
                f'+Si la letra tiene debajo un "*", la letra se encuentra en la palabra pero está mal colocada\n'
                f'+Si la letra tiene debajo un "_", la letra no se encuentra en la palabra')
        return text, f, palabra
    else:
        palabra = 'Guess'
        f = open(WORDS_PATH + WORDS_ENG, "r")
        text = (f'Welcome to Wordle, you will try to guess the word in {NUM_GUESSES} attempts.\n'
                f'Instructions: \n'
                f'+ Each guess must be a {NUM_LETTERS} letter word\n'
                '+ For each letter, if the letter has a "o" under it, the letter is in the word and in the correct spot\n'
                '+ If the letter has a "*" under it, the letter is in the word but in the wrong spot\n'
                '+ If the letter has a "_" under it, the letter is not in the word')
        return text, f, palabra


def guess_word(i, term):
    guess = input(f'{term} {i+1}: ').lower()

    if len(guess) != NUM_LETTERS:
        if LANGUAGE == 'español':
            print(f'Tu intento debe tener una longitud de {NUM_LETTERS} letras')
            return guess_word(i, term)
        else:
            print(f'Your guess must be {NUM_LETTERS} letters long')
            return guess_word(i, term)

    elif any((invalid := letter) not in string.ascii_letters for letter in guess):
        if LANGUAGE == 'español':
            print(f"Carácter inválido: '{invalid}'. Por favor usa sólo letras del español.")
            return guess_word(i, term)
        else:
            print(f"Invalid letter: '{invalid}'. Please use English letters.")
            return guess_word(i, term)

    return guess


def show_guess(guess, word_dict, word):
    guess_result = ['_' for _ in range(NUM_LETTERS)]
    matched_positions = set()

    for c in range(NUM_LETTERS):
        guess_c = guess[c]
        if guess_c in word_dict and c in word_dict[guess_c]:
            guess_result[c] = 'o'
            matched_positions.add(c)

    for c in range(NUM_LETTERS):
        guess_c = guess[c]
        if guess_result[c] != 'o' and guess_c in word_dict:
            for pos in word_dict[guess_c]:
                if pos not in matched_positions:
                    guess_result[c] = '*'
                    matched_positions.add(pos)

    if str(guess) == str(word).lower():
        return 'SOLVED', guess_result
    return guess, guess_result


def game_over(word):
    if LANGUAGE == 'español':
        print(f"No lograste adivinar en {NUM_GUESSES}intentos. La palabra era: {word.lower()}")
        return
    else:
        print(f"You didn't guess in 6 attempts. The word was: {word.lower()}")
        return


def main():
    text, f, term = language_select()
    print(text)

    word_dict, word = get_word(f)

    for i in range(NUM_GUESSES):
        guess = guess_word(i, term)

        guess, guess_result = show_guess(guess, word_dict, word)
        if guess == 'SOLVED':
            if LANGUAGE == 'español':
                print(word)
                print(''.join(guess_result))
                print(f'¡Lo adivinaste en {i + 1} intentos!')
                return
            else:
                print(word)
                print(''.join(guess_result))
                print(f'You got it in {i + 1} attempts!')
                return
        else:
            print(guess)
            print(''.join(guess_result))
    game_over(word)


if __name__ == "__main__":
    random.seed(42)
    NUM_LETTERS = 5
    NUM_GUESSES = 6
    WORDS_PATH = "C:\\Users\\roxan\\rox\\4th\\Proyectos\\"
    WORDS_ENG = "wordle_eng.txt"
    WORDS_ESP = "wordle_esp.txt"
    LANGUAGE = input('inglés o español: ')
    main()
