# Config
- APPLICATION_CONFIG is strictly related to my project and is used only to load a JSON configuration file with the name specified in the variable itself.
- FLASK_CONFIG is used to select the Python object that contains the configuration for the Flask application (see application/app.py and application/config.py). The value of the variable is converted into the name of a class.
- FLASK_ENV is a variable used by Flask itself, and its values are dictated by it. See the configuration documentation mentioned in the resources of the previous section.
- Config database: SQLALCHEMY_DATABASE_URI = (
        f"postgresql+psycopg2://ogwsmojrynkhmc:5e3f5b888472b53141e050ea3e366765203feab53b43a13248b65f718e477e63@ec2-52-86-2-228.compute-1.amazonaws.com:5432/dg0q8kfl0thi4"
    )

- pg_dump -U admin -h localhost -p 5432 --clean -F p trading_system > trading_system1.sql // The default output format of pg_dump is actually plaintext sql script
- psql -U ogwsmojrynkhmc -h ec2-52-86-2-228.compute-1.amazonaws.com -p 5432 -d dg0q8kfl0thi4 < trading_system1.sql

ogwsmojrynkhmc:5e3f5b888472b53141e050ea3e366765203feab53b43a13248b65f718e477e63@ec2-52-86-2-228.compute-1.amazonaws.com:5432/dg0q8kfl0thi4"

# Run the app
1. Give permission to manage.py
- chmod 775 manage.py
2. Create venv
- sudo apt-get install python3-venv
- sudo apt-get install python3-tk
- python3 -m venv .venv
- source .venv/bin/activate
- pip3 install -r requirements/development.txt
- python3 -m pip install <package>
- pip3 freeze > requirements.txt
2. Init database
- ./manage.py flask db init
- ./manage.py flask db stamp head
- ./manage.py flask db migrate
- ./manage.py flask db upgrade
3. Update database
- ./manage.py flask db stamp head
- ./manage.py flask db migrate
- ./manage.py flask db upgrade
4. Run flask with config
- Run by flask command line: FLASK_CONFIG="development" flask run
- Run with manage.py: ./manage.py flask run
5. Build the image
- FLASK_ENV="development" FLASK_CONFIG="development" docker-compose -f docker/development.yml build web
- If you need to explore the container you can login directly with

docker exec -it docker_web_1 bash

or with

FLASK_ENV="development" FLASK_CONFIG="development" docker-compose -f docker/development.yml exec web bash

- To tear down the containers, when running as daemon, you can run

FLASK_ENV="development" FLASK_CONFIG="development" docker-compose -f docker/development.yml down

- If you need to explore the container you can login directly with

$ docker exec -it docker_web_1 bash

or with

$ FLASK_ENV="development" FLASK_CONFIG="development" docker-compose -f docker/development.yml exec web bash

- Run ./manage.py compose up -d and ./manage.py compose down and have the environment variables automatically passed to the system

# Install package
- python3 -m pip install flask_jwt_extended
- python3 -m pip install flask_mail
- python3 -m pip install marshmallow
- python3 -m pip install webargs
# Unit test
- Run pytest

# Notes
- Need to install: sudo apt-get install libpq-dev before installing the 'psycopg2' library
- Permission Denied for docker-compose: try with sudo