# Casting Agency

[Hosted on Heroku at :https://fsdn-casting-agency.herokuapp.com/](https://fsdn-casting-agency.herokuapp.com/)

The motivation for this project is to create my capstone project for Udacity's Fullstack Nanodegree program.
It models a company that is responsible for creating movies and managing and assigning actors to those movies.

## Project dependencies

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

Working within a virtual environment is recommended.

#### PIP Dependencies

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

- you may need to change the database url in setup.sh after which you can run
```bash
source setup.sh
```

- Start server by running
```bash
flask run
```

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server.

- [Pycodestyle](https://pypi.org/project/pycodestyle/) - pycodestyle is a tool to check your Python code against some of the style conventions in PEP 8.


#### Authentication

Authentication is implemented using Auth0, it uses RBAC to assign permissions using roles, these are tokens you could use to access the endpoints.
Note: The tokens expires in 24 hours you can create your own tokens at [Auth0](https://auth0.com/). you would need to refelct this in setup.sh

> Casting Assistant
- Can view actors and movies

> Casting Director
- All permissions a Casting Assistant has and???
- Add or delete an actor from the database
- Modify actors or movies

>Executive Producer
- All permissions a Casting Director has and???
- Add or delete a movie from the database


## Database Setup
The project uses Postgresql as its database, you would need to create one locally and reflect it in setup.sh.
To update the database and seed run the following :
```bash
python manage.py db upgrade
python manage.py seed
```


## Testing
Ensure a test database is created and reflectd in setup.sh.
To start tests, run
```
source test.sh
```


## Documentation
The Endpoints were documented using postman collections
- open `casting-agency-heroku.postman_collection.json` in postman to test with live url on heroku
- open `casting-agency-local.postman_collection.json` in postman to test with Localhost

Note: The tokens used would expire in 24hrs, use your own token as described in the Athentication section.

### Error Handling

- 401 errors due to RBAC are returned as

```json
    {
      "code": "unauthorized",
      "description": "Permission not found."
    }
```


Other Errors are returned in the following json format:

```json
      {
        "success": "False",
        "error": 422,
        "message": "Unprocessable entity",
      }
```

The error codes currently returned are:

* 400 ??? bad request
* 401 ??? unauthorized
* 404 ??? resource not found
* 422 ??? unprocessable
* 500 ??? internal server error



### Endpoints

#### GET /movies

- General:
  - Returns all the movies.
  - Roles authorized : Casting Assistant,Casting Director,Executive Producer.

- Sample:  `curl http://127.0.0.1:5000/movies`

```json
{
    "movies": [
        {
            "id": 1,
            "release_date": "Mon, 06 May 2019 00:00:00 GMT",
            "title": "Terminator Dark Fate"
        },
        {
            "id": 2,
            "release_date": "Tue, 06 May 2003 00:00:00 GMT",
            "title": "Terminator Rise of the machines"
        }
    ],
    "success": true
}
```

#### GET /movies/\<int:id\>

- General:
  - Route for getting a specific movie.
  - Roles authorized : Casting Assistant,Casting Director,Executive Producer.

- Sample:  `curl http://127.0.0.1:5000/movies/1`

```json
{
    "movie": {
        "id": 1,
        "release_date": "Mon, 06 May 2019 00:00:00 GMT",
        "title": "Terminator Dark Fate"
    },
    "success": true
}
```

#### POST /movies

- General:
  - Creates a new movie based on a payload.
  - Roles authorized : Executive Producer.

- Sample: `curl http://127.0.0.1:5000/movies -X POST -H "Content-Type: application/json" -d '{
	"title": "Natasha romanov",
	"release_date": "2020-05-06"
}'`

```json
{
    "movie": {
        "id": 3,
        "release_date": "Wed, 06 May 2020 00:00:00 GMT",
        "title": "Natasha romanov"
    },
    "success": true
}
```

#### PATCH /movies/\<int:id\>

- General:
  - Patches a movie based on a payload.
  - Roles authorized : Casting Director, Executive Producer.

- Sample: `curl http://127.0.0.1:5000/movies/3 -X POST -H "Content-Type: application/json" -d '{
	"title": "Natasha romanov patched",
	"release_date": "2020-05-06"
}'`

```json
{
    "movie": {
        "id": 3,
        "release_date": "Wed, 06 May 2020 00:00:00 GMT",
        "title": "Natasha romanov patched"
    },
    "success": true
}
```


#### DELETE /movies/<int:id\>


- General:
  - Deletes a movies by id form the url parameter.
  - Roles authorized : Executive Producer.

- Sample: `curl http://127.0.0.1:5000/movies/3 -X DELETE`

```json
{
    "message": "movie id 3, titled Natasha romanov patched was deleted",
    "success": true
}
```

#### GET /actors

- General:
  - Returns all the actors.
  - Roles authorized : Casting Assistant,Casting Director,Executive Producer.

- Sample:  `curl http://127.0.0.1:5000/actors`

```json
{
    "actors": [
        {
            "age": 40,
            "gender": "male",
            "id": 1,
            "name": "Will Smith"
        },
        {
            "age": 50,
            "gender": "male",
            "id": 2,
            "name": "Bruce Wills"
        }
    ],
    "success": true
}
```

#### GET /actors/\<int:id\>

- General:
  - Route for getting a specific actor.
  - Roles authorized : Casting Assistant,Casting Director,Executive Producer.

- Sample:  `curl http://127.0.0.1:5000/actors/1`

```json
{
    "actor": {
        "age": 40,
        "gender": "male",
        "id": 1,
        "name": "Will Smith"
    },
    "success": true
}
```

#### POST /actors

- General:
  - Creates a new actor based on a payload.
  - Roles authorized : Casting Director,Executive Producer.

- Sample: `curl http://127.0.0.1:5000/actors -X POST -H "Content-Type: application/json" -d '{
	"name": "Mary",
	"age": 22,
	"gender": "female"
}'`

```json
{
    "actor": {
        "age": 22,
        "gender": "female",
        "id": 3,
        "name": "Mary"
    },
    "success": true
}
```

#### PATCH /actors/\<int:id\>

- General:
  - Patches an actor based on a payload.
  - Roles authorized : Casting Director, Executive Producer.

- Sample: `curl http://127.0.0.1:5000/actors/3 -X POST -H "Content-Type: application/json" -d '{
	"name": "John",
	"age": 22,
	"gender": "female"
}'`

```json
{
    "actor": {
        "age": 22,
        "gender": "female",
        "id": 3,
        "name": "John"
    },
    "success": true
}
```


#### DELETE /actors/<int:id\>


- General:
  - Deletes an actor by id form the url parameter.
  - Roles authorized : Casting Director,Executive Producer.

- Sample: `curl http://127.0.0.1:5000/actors/3 -X DELETE`

```json
{
    "message": "actor id 3, named John was deleted",
    "success": true
}
```

## Authors
- Udacity provided the specifications
- Hossam Reda Implemented the application