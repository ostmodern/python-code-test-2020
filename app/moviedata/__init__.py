import omdb

from django.conf import settings

omdb.set_default('apikey', settings.OMDB_API_KEY)
