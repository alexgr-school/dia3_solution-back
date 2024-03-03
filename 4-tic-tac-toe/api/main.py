from flask import Flask
import config
from routes import register_routes
from tic_tac_toe import TicTacToe

app = Flask(__name__)
config.init_cors(app)
game = TicTacToe()  # Création de l'instance de jeu ici
register_routes(app, game)

if __name__ == '__main__':
    app.run(debug=True, port=8080)
