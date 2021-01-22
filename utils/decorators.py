from datetime import datetime
from flask import abort, current_app, request, Response, make_response
from functools import update_wrapper, wraps


def no_cache(view):
    """
    Tell the client that this view should never be cached (useful for docs)
    """
    cache_control = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'

    @wraps(view)
    def decorator(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        response.headers['Last-Modified'] = datetime.now()
        response.headers['Cache-Control'] = cache_control
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '-1'
        return response

    return update_wrapper(decorator, view)
