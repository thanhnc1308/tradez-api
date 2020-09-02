# Config
- APPLICATION_CONFIG is strictly related to my project and is used only to load a JSON configuration file with the name specified in the variable itself.
- FLASK_CONFIG is used to select the Python object that contains the configuration for the Flask application (see application/app.py and application/config.py). The value of the variable is converted into the name of a class.
- FLASK_ENV is a variable used by Flask itself, and its values are dictated by it. See the configuration documentation mentioned in the resources of the previous section.

# Run the app
1. Give permission to manage.py
- chmod 775 manage.py
2. Init database
./manage.py flask db init
- creating models we will use the commands 
./manage.py flask db migrate 
./manage.py flask db upgrade
2. Run flask with config
- Run by flask command line: FLASK_CONFIG="development" flask run
- Run with manage.py: ./manage.py flask run
3. Build the image
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

# Notes
- Need to install: sudo apt-get install libpq-dev before installing the 'psycopg2' library
- Permission Denied for docker-compose: try with sudo
- Redundant dependencies:
distro-info===0.23ubuntu1
duplicity==0.8.12.0
language-selector==0.1
louis==3.12.0
python-apt==2.0.0+ubuntu0.20.4.1
python-debian===0.1.36ubuntu1
systemd-python==234
typed-ast==1.4.1
ubuntu-advantage-tools==20.3
toml==0.10.1
ubuntu-drivers-common==0.0.0
SQLAlchemy==1.3.19