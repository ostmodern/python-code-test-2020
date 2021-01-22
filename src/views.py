import uuid
from typing import Mapping

import requests
from flask import jsonify, request, send_from_directory
from flask.views import MethodView

from settings import OMDB_APIKEY, OMDB_BASE_URL
from src.models import Comment, Episode, Movie
from utils import decorators


def get_episodes():
    title = request.args.get('title', 'Game of Thrones')
    url = f'{OMDB_BASE_URL}?t={title}&apikey={OMDB_APIKEY}'
    movie_info = requests.get(url)
    total_seasons = int(movie_info.json().get('totalSeasons', 0))
    movie_imdb_id = movie_info.json().get('imdbID')
    movies_model = Movie()
    movies_model.insert_one(movie_info.json())

    if total_seasons:
        for season_number in range(1, total_seasons + 1):
            season_url = f"{OMDB_BASE_URL}/?t={title}&Season={season_number}&apikey={OMDB_APIKEY}"
            season = requests.get(season_url).json().get('Episodes')
            for episode in season:
                episode.update({'movieImdbID': movie_imdb_id})
                episode.update({'Season': season_number})
                episodes_model = Episode()
                episodes_model.insert_one(episode)

    return jsonify({'message': f'All episodes of {title} are in database now.'})


class Episodes(MethodView):

    def get(self, imdb_id=None):
        model = Episode()
        best_episodes = request.args.get('best_episodes', 0)
        season = request.args.get('season')
        query = {'imdbRating': {'$gt': '8.8'}} if best_episodes else {}
        if season:
            query.update(
                {'Season': int(season)}
            )
        result = model.find_by_imdb_id(imdb_id) if imdb_id else list(model.find(query))
        response = {
            'episodes': result,
            'total': len(result) if isinstance(result, list) else 1}
        return jsonify(response)


class Comments(MethodView):
    model = Comment()

    def post(self):
        request_data = dict(request.json) if request.json else dict()
        data = self.validate(request_data)
        if 'errors' not in data:
            self.model.insert_one(data)
            status_code = 200
        else:
            status_code = 400
        return jsonify(data), status_code

    def get(self, imdb_id):
        result = list(self.model.find({'imdbID': imdb_id}))
        if len(result):
            response, status_code = {'comments': result, 'total': len(result)}, 200
        else:
            response, status_code = {'error': 'No comments or wrong imdbID provided'}, 400
        return jsonify(response), status_code

    def patch(self):
        data = request.json or {}
        if 'comment_id' not in data:
            return jsonify({'comment_id': 'This is required field'}), 400
        if 'body' not in data:
            return jsonify({'body': 'This field is required'}), 400
        comment_id = self.ensure_uuid(data['comment_id'])
        if not isinstance(comment_id, uuid.UUID):
            return jsonify({'error': 'Wrong comment_id'}), 400
        body = {'body': data['body']}
        result = self.model.update(comment_id, body)
        if result:
            response, status_code = {'message': 'Comment successfully updated.'}, 200
        else:
            response, status_code = {'error': 'Something went wrong'}, 400
        return jsonify(response), status_code

    def delete(self):
        data = request.json or {}
        if 'comment_id' not in data:
            return jsonify({'comment_id': 'This is required field'}), 400
        comment_id = self.ensure_uuid(data['comment_id'])
        if not isinstance(comment_id, uuid.UUID):
            return jsonify({'error': 'Wrong comment_id'}), 400
        result = self.model.delete_one(comment_id)
        if result:
            response, status_code = {'message': 'Comment successfully deleted.'}, 200
        else:
            response, status_code = {'error': 'Something went wrong'}, 400
        return jsonify(response), status_code

    def validate(self, data):
        errors = []
        if not isinstance(data, Mapping):
            errors.append({'error': 'Data should be dict-like object'})
        if 'body' not in data:
            errors.append({'body': 'This field is required'})
        if 'imdbID' not in data:
            errors.append({'imdbID': 'This field is required'})
        episode_model = Episode()
        episode = episode_model.find_by_imdb_id(data.get('imdbID'))
        if not episode:
            errors.append({'imdbID': 'Episode with this imdbID does not exist.'})
        if 'author' not in data:
            errors.append({'author': 'This field is required'})
        return {'errors': errors} if errors else data

    @staticmethod
    def ensure_uuid(value):
        if not isinstance(value, uuid.UUID):
            try:
                value = uuid.UUID(value)
            except (TypeError, ValueError):
                return None
        return value



@decorators.no_cache
def serve_swagger_docs_yaml():
    return send_from_directory('docs', 'doc.yml')


@decorators.no_cache
def serve_docs_ui(path):
    print(path)
    return send_from_directory('swagger', path)
