from flask import Flask, render_template, request, session
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with your own secret key

hangman_stages = [
    '''
       -----
       |   |
           |
           |
           |
           |
    ''',
    '''
       -----
       |   |
       O   |
           |
           |
           |
    ''',
    '''
       -----
       |   |
       O   |
       |   |
           |
           |
    ''',
    '''
       -----
       |   |
       O   |
      /|   |
           |
           |
    ''',
    '''
       -----
       |   |
       O   |
      /|\\  |
           |
           |
    ''',
    '''
       -----
       |   |
       O   |
      /|\\  |
      /    |
           |
    ''',
    '''
       -----
       |   |
       O   |
      /|\\  |
      / \\  |
           |
    '''
]

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'attempts' not in session:
        session['attempts'] = 6
    if 'guessed_letters' not in session:
        session['guessed_letters'] = []
    if 'chosen_word' not in session:
        word_list = ['python', 'java', 'ruby', 'javascript', 'html', 'css', 'csharp', 'golang', 'kotlin', 'swift']
        session['chosen_word'] = random.choice(word_list)
    if 'message' not in session:
        session['message'] = ''
    
    if request.method == 'POST':
        guess = request.form.get('guess')
        if guess.isalpha() and len(guess) == 1:
            if guess in session['guessed_letters']:
                session['message'] = 'You have already guessed that letter, try again.'
            elif guess not in session['chosen_word']:
                session['message'] = 'The letter is not in the word.'
                session['guessed_letters'].append(guess)
                session['attempts'] -= 1
            else:
                session['message'] = 'Well done, that letter exists in the word!'
                session['guessed_letters'].append(guess)
        else:
            session['message'] = 'Invalid input, please try again.'
    
    hangman_stage = hangman_stages[6 - session['attempts']]
    
    return render_template('index.html', attempts=session['attempts'], message=session['message'], guessed_letters=session['guessed_letters'], chosen_word=session['chosen_word'], hangman_stage=hangman_stage)

if __name__ == "__main__":
    app.run(debug=True)

