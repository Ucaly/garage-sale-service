# Garage Sale service

This project is designed for an individual who wants to sell own items online.

## Getting Started

### Installing Dependencies

#### Python 3.8

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

Setting up a virtual environment is recommended. Instructions for setting up a virual enviornment can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once virtual environment setup and running, install dependencies by running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
To setup database locally, replace with your db user for `DB_USESRNAME` in setup.sh.  With Postgres running, create a database named `garagesale`. Run migration scripts to populate tables.  Feed sample data using the garagesale.psql file provided. From the root directory in terminal run:
```bash
source setup.sh
createdb garagesale
python manage.py db upgrade
psql garagesale < garagesale.psql
```

## Running the server

### Backend
From within the `garage-sale-service` start the service:

```bash
flask run
```

`FLASK_ENV` variable is set to `development` in `.env` file.  This setting will detect file changes and restart the server automatically.

If running locally on Windows, refer to [Flask documentation](https://flask.palletsprojects.com).

The service is run on http://127.0.0.1:5000 locally by default.

### Frontend

Frontend code is availabe at: https://github.com/Ucaly/garage-sale-ui

By default, the frontend will run on https://127.0.0.1:3000.


## API Refrence

### Refere to [API Reference](./API.md)

## Testing

To run unit tests locally, re-create local database.  Open 'setup.sh' file and update the database user name for DB_USESRNAME as per your environment. Drop existing database then create a new one. 
Dump the sample psql file using the command 'psql garagesale_test < test_garagesale.psql'
Export environment variables by running the setup.sh file:

Bavigate to the project root directory and run the following commands to setup test database:
```
source setup.sh
dropdb gragesale
createdb garagesale
python manage.py db upgrade
psql garagesale < garagesale.psql
```

Finally execute tests:
```
python test_suite.py
```
