from app.models import Comment, Episode


def test_new_episode():
    episode = Episode(        
            imdb_id='tt14899995',
            imdb_rating=9.9,
            released='2011-04-17',
            season=1,
            title='Test episode',
    )
    assert episode.imdb_id == 'tt14899995'
    assert episode.imdb_rating == 9.9
    assert episode.released == '2011-04-17'
    assert episode.season == 1
    assert episode.title == 'Test episode'

def test_new_comment():
    comment = Comment(
        text='Generated comment',
        episode_id=3
    )
    assert comment.text == 'Generated comment'

    assert comment.episode_id == 3
