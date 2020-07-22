# Ostmodern Python Code Test

The goal of this exercise is to test if you know your way around developing 
REST APIs in Python using docker. You can use any rest framework and database 
of your choice. Approach it the way you would an actual long-term project.

To start with, a Dockerfile (with Python3.7 Apline image) has been provided for you.
A docker-compose file with stubs for a sample SQL and a NoSQL database has been provided. 
Feel free to change it as per your choice of database.


## Tasks

Your task is to build a JSON-based REST API for your frontend developers to
consume. You have built a list of user stories with your colleagues, but you get
to decide how to design the API. Remember that the frontend developers will need
some documentation of your API to understand how to use it.

We do not need you to implement users or authentication, to reduce the amount of
time this exercise will take to complete. 

* Ability to import all episodes of all seasons of `Game of Thrones` from [OMDb API](http://www.omdbapi.com/).
(You will have to get an APIKey from http://www.omdbapi.com/apikey.aspx to use their API)
The APIs that may be used are:
 http://www.omdbapi.com/?t=Game of Thrones&Season=1&apikey=<api key>
 http://www.omdbapi.com/?i=tt1480055&apikey=<api key> (for an episode)
* Design the data model to store this data.
* An GET API to list episodes where `imdbRating` is greater than 8.8 for a season or all seasons.
* Write some unit tests
* Remember that the frontend developers will need
some documentation of your API to understand how to use it.
