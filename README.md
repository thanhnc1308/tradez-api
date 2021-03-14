# Config
- APPLICATION_CONFIG is strictly related to my project and is used only to load a JSON configuration file with the name specified in the variable itself.
- FLASK_CONFIG is used to select the Python object that contains the configuration for the Flask application (see application/app.py and application/config.py). The value of the variable is converted into the name of a class.
- FLASK_ENV is a variable used by Flask itself, and its values are dictated by it. See the configuration documentation mentioned in the resources of the previous section.

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

# To learn
@wraps(func)
    def wrapper(*args, **kwargs):
make_response
decorators
@staticmethod
@property
updated_at = db.Column(db.DateTime(), nullable=False, default=lambda: datetime.utcnow())
created_at = db.Column(db.DateTime(), nullable=False, default=lambda: datetime.utcnow())
def __init__(self,*args,**kwargs):
from flask_login import login_required, login_user, logout_user
from werkzeug.security import check_password_hash
@functools.wraps(func)
    def wrapper(*args, **kwargs):
@post_load
from opbeat.contrib.flask import Opbeat
opbeat = Opbeat()

# Done
- paging_filter, flask-httpauth, reference column
https://github.com/joshfriend/flask-restful-demo
- StockController: Schema marshmallow, api blueprint
https://github.com/erdem/flask-restful-example
- pytest
https://github.com/alexandre-old/flask-rest-template
- MongoEngine
https://github.com/alexandre-old/flask-rest-template
- middlewares and admin
https://github.com/solnsumei/flask-rest-api-setup

# Problems
- The following paths are ignored by one of your .gitignore files: dbconfig Use -f if you really want to add them.
git check-ignore -v -f dbconfig
