from flask import Flask
from home.view import home
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///server_inventory_bootstrap.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "random string"

db = SQLAlchemy(app)

app.register_blueprint(home)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
