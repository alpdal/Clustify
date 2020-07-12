from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
from flask_session import Session
from flask_assets import Environment
from .assets import compile_static_assets


# Globally accessible instances
sess = Session()
assets = Environment()

def create_app():
    # Initialize the core application
    application = Flask(__name__, instance_relative_config=False)
    application.config.from_object("config.Config")


    # Initialize plugins
    sess.init_app(application)
    assets.init_app(application)

    with application.app_context():
        # include routes
        from .main import main_routes
        # register blueprints
        application.register_blueprint(main_routes.main_bp)

        compile_static_assets(assets)

        return application
