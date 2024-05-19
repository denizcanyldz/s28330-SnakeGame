from flask import Flask, render_template, request, redirect, url_for, session
from pymongo import MongoClient
import certifi
from snake_game import game

app = Flask(__name__, static_folder='static')
app.secret_key = 'b\xd7\xde\xb0\x17}\x7f\x98\x08Em\xe1\xd9Ev'

allowed_characters = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_")  #

MONGODB_URL = "mongodb+srv://deniz:denizpjatk@cluster0.5y1k84l.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(MONGODB_URL, tlsCAFile=certifi.where())
db = client['snake_game']


def save_game_score(user_name, score):
    scores_collection = db.scores  # 'scores' is the collection
    scores_collection.insert_one({"user_name": user_name, "score": score})


def get_high_scores(limit=10):
    scores_collection = db.scores
    return list(scores_collection.find().sort("score", -1).limit(limit))


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        size = int(request.form['size'])  # Get the size from the form
        name = request.form['name']  # Capture the name from the form
        if 5 <= size <= 25:
            session['user_name'] = name  # Store the user's name in the session
            game.init_game(size, size, name)  # Initialize the game with size and name
            return redirect(url_for('game_view'))  # Redirect to the game view
        else:
            return render_template('index.html',
                                   error="Size must be between 5 and 25.")  # Show error if size is out of bounds
    return render_template('index.html')  # Show the index page for GET requests


@app.route('/game', methods=['GET', 'POST'])
def game_view():
    if request.method == 'POST':
        if 'direction' in request.form:
            game.change_direction(request.form['direction'])
    if game.is_game_over():
        return redirect(url_for('game_over'))
    game.move_snake()
    return render_template('game.html', snake=game.get_snake(), food=game.get_food(), board=game.get_board(),
                           walls=game.get_walls())


@app.route('/game_over')
def game_over():
    score = len(game.get_snake()) - 3  # Calculate the score, assuming the initial length is 3
    user_name = session.get('user_name', 'Anonymous')  # Retrieve the name from the session, default to 'Anonymous'
    save_game_score(user_name, score)  # Save the score with the user's name
    return render_template('game_over.html', score=score,
                           user_name=user_name)  # Pass the score and name to the template


@app.route('/high_scores')
def high_scores():
    scores = get_high_scores()
    return render_template('high_scores.html', scores=scores)


if __name__ == "__main__":
    app.run(debug=True)
