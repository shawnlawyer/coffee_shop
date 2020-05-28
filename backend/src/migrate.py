from flask import Flask
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_sqlalchemy import SQLAlchemy
import os

database_filename = os.path.join("database","database.db")
project_dir = os.path.dirname(os.path.abspath(__file__))
database_path = "sqlite:///{}".format(os.path.join(project_dir, database_filename))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_path
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

class Drink(db.Model):

    id = db.Column(db.Integer().with_variant(db.Integer, "sqlite"), primary_key=True)
    title = db.Column(db.String(80), unique=True)
    recipe =  db.Column(db.String(180), nullable=False)


if __name__ == '__main__':
    manager.run()
