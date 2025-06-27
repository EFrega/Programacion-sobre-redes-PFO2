from flask import Flask
from db import init_db
from api import api

app = Flask(__name__)
app.register_blueprint(api)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)