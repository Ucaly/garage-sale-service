# Garage Sale service

This project is designed for an individual who wants to sell own items online.  

## Getting Started

### Installing Dependencies

#### Python 3.8

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the garagesale.psql file provided. From the backend folder in terminal run:
```bash
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

The service is run on http://127.0.0.1:5000 locally by default.  This URL is set as a proxy in the frontend configuration.

### Frontend

From within the `frontend` directory, run the following commands to start the client:

```bash
yarn dev
```

By default, the frontend will run on https://127.0.0.1:3000.


## API Refrence

### Refere to [API Reference](./API.md)

## Testing
In order to run tests, navigate to the backend directory and run the following commands to setup test database:
```
dropdb garagesale_test
createdb garagesale_test
psql garagesale_test < garagesale.psql
```

Then set database user name:
```
export DB_USERNAME='user_name'
```

Finally run tests:
```
python test_garagesale.py
```
