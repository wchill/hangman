from __future__ import print_function
import random
import sys

# Make this program work on both python 2 and 3
if sys.version_info[0] < 3:
    input = raw_input

HANGMAN_TEMPLATE = """
 +--------+
 |        |
 |        0
 |       213
 |        1
 |       4 5
 |
-+-----------
"""

HANGMAN_BODY_PARTS = 'O|\\//\\'

# Load a random word from the wordlist using reservoir sampling
def get_random_word_from_wordlist():
    # type: () -> Text

    selected = None

    with open('words.txt', 'r') as f:
        for index, line in enumerate(f):
            if selected is None:
                selected = line
            else:
                r = random.randint(0, index)
                if r == 0:
                    selected = line

    return selected.strip().upper()

# Take the number of incorrect guesses and return a string representing the correct hangman
def draw_hangman(num_parts):
    # type: (Number) -> Text

    result = HANGMAN_TEMPLATE
    for index, ch in enumerate(HANGMAN_BODY_PARTS):
        substitute_char = ch if num_parts > index else ' '
        result = result.replace(str(index), substitute_char)
    return result

# Take a word, a list with the state of the correct letters, and a list with the incorrect guesses
# and return a string representing the guessed letters
def draw_word_state(word, correct_guesses, incorrect_guesses):
    # type: (Text, List[bool], List[Text]) -> Text

    str_buffer = []

    for index, ch in enumerate(word):
        if correct_guesses[index]:
            str_buffer.append('_' + ch.upper() + '_')
        else:
            str_buffer.append('___')

    result = ' '.join(str_buffer)

    incorrect_guesses_upper = [ch.upper() for ch in incorrect_guesses]

    result += '\r\n\r\nIncorrect guesses: %s' % ' '.join(incorrect_guesses_upper)

    return result

# Take a word, a list with the state of the correct letters, and a guess
# and return the number of letters guessed successfully
def guess_letter(word, correct_guesses, guess):
    # type: (Text, List[bool], Text) -> Number

    correct = 0

    for index, ch in enumerate(word):
        if guess.upper() == ch.upper():
            correct_guesses[index] = True
            correct += 1

    return correct

def main():
    print('Welcome to Hangman!')

    word = get_random_word_from_wordlist()
    correct = [False for _ in word]
    incorrect = []
    guessed = set()

    try:
        while True:
            print('=' * 80)
            print('')
            print(draw_hangman(len(incorrect)))
            print(draw_word_state(word, correct, incorrect))

            if all(correct):
                print('Congratulations, you guessed the word!')
                exit(0)

            if len(incorrect) >= len(word):
                print('You lose! The word was %s' % word)
                exit(1)

            print('')
            guess = input('Guess a letter: ')

            if len(guess) != 1 or not ('a' <= guess <= 'z' or 'A' <= guess <= 'Z') or guess in guessed:
                print('That\'s not a valid guess.')
                continue

            guessed.add(guess)

            if guess_letter(word, correct, guess) == 0:
                incorrect.append(guess)
                print('You guessed wrong!')
            else:
                print('You guessed a letter correctly!')

    except KeyboardInterrupt:
        print('Quitter!')
        exit(1)

if __name__ == '__main__':
    main()
