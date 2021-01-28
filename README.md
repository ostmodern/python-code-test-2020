Endpoints:

%HOSTNAME%/episodes/
%HOSTNAME%/episode/id> e.g http://0.0.0.0/episode/2

%HOSTNAME%/episodes/ also supports 'min_rating' query_param for showing only episodes greater than passed value,  e.g http://0.0.0.0/episodes/?min_rating=9.0


docker-compose exec web pytest .