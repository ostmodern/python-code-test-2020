import json
from flask import Flask

from src import views

app = Flask(__name__)
app.url_map.strict_slashes = False

app.add_url_rule('/get-episodes', methods=['GET'],
                 view_func=views.get_episodes)

app.add_url_rule('/episodes', methods=['GET'],
                 view_func=views.Episodes.as_view('episodes'))
app.add_url_rule('/episodes/<string:imdb_id>', methods=['GET'],
                 view_func=views.Episodes.as_view('episode'))

app.add_url_rule('/episodes/<string:imdb_id>/comments', methods=['GET'],
                 view_func=views.Comments.as_view('episodes_comments'))

app.add_url_rule('/comments', methods=['POST', 'PATCH', 'DELETE'],
                 view_func=views.Comments.as_view('comments'))

# SWAGGER
app.add_url_rule('/apidocs.yml', view_func=views.serve_swagger_docs_yaml)
app.add_url_rule('/docs', view_func=views.serve_docs_ui,
                 defaults={'path': 'index.html'})
app.add_url_rule('/docs/<path:path>', view_func=views.serve_docs_ui)

