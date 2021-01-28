import json
import pytest

from app.views import (
    episodes_retrieve_all,
    episode_retrieve_one,
    comments_retrieve_all,
    comment_retrieve_one,
    comment_delete_one,
    comment_update_one,
    comment_create_one,
)