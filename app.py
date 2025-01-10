from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///strategy_tester.db"
    db.init_app(app)
    migrate.init_app(app, db)

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
