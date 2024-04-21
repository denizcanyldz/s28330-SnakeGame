from flask import Flask, render_template, request, redirect, url_for

from Game.snake_game import game

app = Flask(__name__)
allowed_characters = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_")


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        width = int(request.form['width'])
        height = int(request.form['height'])
        name = request.form['name']
        if 5 <= width <= 25 and 5 <= height <= 25:
            game.init_game(width, height, name)
            return redirect(url_for('game_view'))
        else:
            return render_template('index.html', error="Width and height must be between 5 and 25.")
    return render_template('index.html')


@app.route('/game', methods=['GET', 'POST'])
def game_view():
    if request.method == 'POST':
        if 'direction' in request.form:
            game.change_direction(request.form['direction'])
    if game.is_game_over():
        return redirect(url_for('game_over'))
    game.move_snake()
    return render_template('game.html', snake=game.get_snake(), food=game.get_food(), board=game.get_board(), walls=game.get_walls())


@app.route('/game_over')
def game_over():
    return render_template('game_over.html', score=len(game.get_snake()))


if __name__ == "__main__":
    app.run(debug=True)
