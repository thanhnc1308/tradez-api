import os
from application import create_app
app = create_app(os.environ["FLASK_CONFIG"] or "development")
