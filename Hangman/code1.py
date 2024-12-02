import random

# List of possible words for the game
words = ["python", "java", "kotlin", "javascript", "hangman", "programming", "debugging", "variable"]

def choose_word():
    # Randomly select a word from the list
    return random.choice(words)

def display_game_state(word, guessed_letters):
    # Show the word with guessed letters revealed and others hidden as underscores
    display = [letter if letter in guessed_letters else '_' for letter in word]
    print("Current word: " + ' '.join(display))

def get_user_guess(guessed_letters):
    while True:
        guess = input("Guess a letter: ").lower()
        if len(guess) != 1:
            print("Please enter a single letter.")
        elif not guess.isalpha():
            print("Please enter a valid letter.")
        elif guess in guessed_letters:
            print("You already guessed that letter.")
        else:
            return guess

def play_hangman():
    word = choose_word()  # The word to be guessed
    guessed_letters = set()  # Keep track of guessed letters
    attempts = 6  # Number of attempts player has
    
    print("Welcome to Hangman!")

    while attempts > 0:
        display_game_state(word, guessed_letters)
        guess = get_user_guess(guessed_letters)

        if guess in word:
            print(f"Good job! {guess} is in the word.")
        else:
            attempts -= 1
            print(f"Sorry, {guess} is not in the word. Attempts remaining: {attempts}")
        
        guessed_letters.add(guess)
        
        # Check if the player has guessed all letters in the word
        if all(letter in guessed_letters for letter in word):
            print(f"Congratulations! You've guessed the word: {word}")
            break
    else:
        print(f"Game over! The word was: {word}")

if __name__ == "__main__":
    play_hangman()
