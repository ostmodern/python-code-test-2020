Interactive SwaggerUI is available on http://0.0.0.0/ui/

Endpoints:
GET 0.0.0.0/episodes/ (also supports 'only_best' boolean query_param for showing only episodes with imdb_rating greater than 8.8
GET 0.0.0.0/episode/<id> e.g http://0.0.0.0/episode/2

GET 0.0.0.0/comments/
POST 0.0.0.0/comments/

GET 0.0.0.0/comment/<id>
PATCH 0.0.0.0/comment/<id>
DELETE 0.0.0.0/comment/<id>

%HOSTNAME%/episodes/


To start unit tests, use  
```docker-compose exec backend pytest app```
Tests is only checking consistency of models.

Results:
This project created using Flask/Connexion/Postgresql/Pytest
All basic and additional requirements have been met.

Next steps should be:
- adding functional tests with database & requests checking
- implementing async import
- maybe moving to asynchronous Python web-framework: (FastApi/Quart/Starlette)
All of them now has version number below 1, so i decided to use more stable Flask web-framework
- adding Redis cache
