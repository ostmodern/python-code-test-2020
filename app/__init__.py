import connexion
import logging
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow

from .config import Config

logger = logging.basicConfig(level=logging.INFO)


def init_app():
    app = connexion.FlaskApp(
        __name__,
        port=80,
        specification_dir="../openapi",
        options={"swagger_ui": True},
    )
    app.add_api("spec.yaml", arguments={"title": "Assignment task"})
    app.app.config.from_object(Config)

    db.init_app(app.app)
    migrate.init_app(app=app.app, db=db)
    return app.app


db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()

app = init_app()

with app.app_context():
    from app.commands import import_episodes

    app.cli.add_command(import_episodes)

    db.create_all()
