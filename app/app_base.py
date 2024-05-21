import secrets
from flask import Flask
from flask import Blueprint
import os
import dotenv
from werkzeug.middleware.proxy_fix import ProxyFix
import pathlib
import logging

thisdir = pathlib.Path(__file__).parent

dotenv.load_dotenv()
if os.getenv('FLASK_ENV') != 'production' and thisdir.joinpath('dev.env').exists():
    dotenv.load_dotenv('dev.env', verbose=True, override=True)

FLASK_ENV = os.getenv('FLASK_ENV', 'development')
SECRET_KEY = os.getenv('SECRET_KEY')
if not SECRET_KEY and FLASK_ENV != "production":
    SECRET_KEY = secrets.token_urlsafe(16)

logging.basicConfig(level=logging.WARNING)

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_host=1, x_proto=1)  # Adjust these values according to your setup
bp = Blueprint('acasearch', __name__, static_folder='static', static_url_path='/static')
