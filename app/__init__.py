from flask import Flask
from config import config_options
from flask_bootstrap import Bootstrap
<<<<<<< HEAD
from flask_sqlalchemy import SQLAlchemy

bootstrap = Bootstrap()
db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__)

=======

bootstrap = Bootstrap()

def create_app(config_name):
    app = Flask(__name__)
    
>>>>>>> 86754da7c3d65fd27868b52f7533b96490a3f83e
    app.config.from_object(config_options[config_name])

    bootstrap.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

<<<<<<< HEAD
    return app 
=======
    return app
>>>>>>> 86754da7c3d65fd27868b52f7533b96490a3f83e
