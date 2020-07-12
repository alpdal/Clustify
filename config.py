from os import environ, path
from dotenv import load_dotenv   # install as python-dotenv 
import redis


class Config:

    # Spotify Config
    CLIENT_ID = environ.get("CLIENT_ID")
    CLIENT_SECRET = environ.get('CLIENT_SECRET')
    SESSION_COOKIE_PATH = "/"
    APPLICATION_ROOT = "https://clustify.co"

    # General Config
    DEBUG = environ.get("DEBUG")
    SECRET_KEY = environ.get("SECRET_KEY")

    # Database 
    SQLALCHEMY_DATABASE_URI = "sqlite:///spotify.db"

    # Flask-Session
    SESSION_TYPE = 'redis'
    SESSION_REDIS = redis.from_url(environ.get('SESSION_REDIS'))

    # Port and callback url
    PORT = "8080"
    CALLBACK_URL = "https://clustify.co"

    # Add needed scope from spotify user
    SCOPE = "playlist-read-collaborative playlist-read-private playlist-modify-public playlist-modify-private"

    # Front-end assets
    LESS_BIN = '/usr/local/bin/lessc'
    ASSETS_DEBUG = False
    ASSETS_AUTO_BUILD = True
