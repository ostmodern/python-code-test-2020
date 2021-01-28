import click
from flask.cli import with_appcontext
from app import db
from app.models import Episode

@click.command(name="import_episodes", help="Import all episodes of GoT to database")
@with_appcontext
def import_episodes():
    existing_episodes = db.session.query(Episode).all()
    episodes = get_episodes()

    if len(existing_episodes) >= len(episodes):
        click.echo("Episodes already imported")

    else:
        for row in episodes:
            episode = Episode(
                title=row["Title"],
                released=row["Released"],
                season_num=row["Season"],
                episode_num=row["Episode"],
                imdb_rating=row["imdbRating"],
                imdb_id=row["imdbID"],
            )
            db.session.add(episode)
        try:
            db.session.commit()
            click.echo("Episodes imported")
        except Exception as e:
            db.session.rollback()
            print(f"Exception: {e}")
