from flask import Flask
import config
from routes import register_routes

app = Flask(__name__)
config.init_cors(app)
register_routes(app)

if __name__ == '__main__':
    app.run(debug=True, port=8080)
