from flask import Flask, render_template, request, jsonify
import random
import os

app = Flask(__name__)

words = os.getenv('WORDS_LIST', "python,java,kotlin,javascript,hangman,programming,debugging,variable").split(',')

def choose_word():
    word = random.choice(words)  
    revealed_letter = random.choice(word) 
    return word, revealed_letter

def initialize_game():
    word, revealed_letter = choose_word()
    guessed_letters = [revealed_letter] 

    word_display = [letter if letter == revealed_letter else '_' for letter in word]

    attempts_left = 6
    return {
        "word": word,
        "guessed_letters": guessed_letters,
        "word_display": word_display,
        "attempts_left": attempts_left
    }

game_state = initialize_game()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/guess', methods=['POST'])
def guess():
    letter = request.json['letter'].lower()
    word = game_state['word']
    guessed_letters = game_state['guessed_letters']

    if letter not in guessed_letters:
        guessed_letters.append(letter)
        if letter not in word: 
            game_state['attempts_left'] -= 1

    game_state['word_display'] = [letter if letter in guessed_letters else '_' for letter in word]

    if all(letter in guessed_letters for letter in word):
        return jsonify({"status": "win", "word": word})

    if game_state['attempts_left'] <= 0:
        return jsonify({"status": "lose", "word": word})

    return jsonify({
        "status": "ongoing",
        "word_display": game_state['word_display'],
        "attempts_left": game_state['attempts_left'],
        "guessed_letters": guessed_letters,
    })

@app.route('/reset', methods=['POST'])
def reset():
    global game_state
    game_state = initialize_game() 
    return jsonify({
        "message": "Game reset",
        "word_display": game_state['word_display'],
        "attempts_left": game_state['attempts_left']
    })

if __name__ == '__main__':
    debug_mode = os.getenv('DEBUG', 'False').lower() in ['true', '1', 't']
    app.run(debug=debug_mode)
