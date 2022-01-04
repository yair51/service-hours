# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from .config import DevelopmentConfig, Config, StagingConfig

# app = Flask(__name__)
# db = SQLAlchemy(app)

# app.config.from_object(DevelopmentConfig)

# from .views import views
# from .auth import auth

# app.register_blueprint(views, url_prefix='/')
# app.register_blueprint(auth, url_prefix='/')

from flask import Flask
from flask.helpers import url_for
from flask_sqlalchemy import SQLAlchemy
from os import path, getenv
from flask_login import LoginManager, current_user
from .config import DevelopmentConfig, Config, StagingConfig
from flask_migrate import Migrate
from flask_mail import Mail, Message
from flask import render_template, request, redirect
from flask_admin import Admin
from oauthlib.oauth2 import WebApplicationClient
import requests
from itsdangerous import URLSafeSerializer
import os

GOOGLE_CLIENT_ID = Config.GOOGLE_CLIENT_ID
GOOGLE_CLIENT_SECRET = Config.GOOGLE_CLIENT_SECRET
GOOGLE_DISCOVERY_URL = Config.GOOGLE_DISCOVERY_URL
client = WebApplicationClient(GOOGLE_CLIENT_ID)


db = SQLAlchemy()
migrate = Migrate()
admin = Admin()
mail = Mail()
DB_NAME = "database.db"
s = URLSafeSerializer(Config.SECRET_KEY)


def create_app():
    app = Flask(__name__)
    # sets development/production enviornment
    #env_config = DevelopmentConfig
    env_config = getenv("APP_SETTINGS", "DevelopmentConfig")
    if env_config == 'Config':
        env_config = Config
    elif env_config == 'StagingConfig':
        env_config = StagingConfig
    else:
        env_config = DevelopmentConfig
    print(env_config)
    app.config.from_object(env_config)
    # app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    # app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    # mail config: 
    
    # app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    # app.config['MAIL_PORT'] = 465
    # app.config["MAIL_USE_TLS"]= False
    # app.config['MAIL_USE_SSL'] = True
    # app.config['MAIL_USERNAME'] = 'info.reportthatpantry@gmail.com'
    # app.config['MAIL_PASSWORD'] = 'vrucxrsmpacwcdsk'
    
    # email = Mail(app)

    # @app.route('/sendmail', methods=['GET', 'POST'])
    # def sendmail():
    #     bodyText = 'First name: ' + request.form['fname'] + '\n'
    #     bodyText += 'Last name: ' + request.form['lname'] + '\n'
    #     bodyText += 'Email: ' + request.form['email'] + '\n'
    #     bodyText += 'State: ' + request.form['state'] + '\n'
    #     bodyText += 'Message: ' + request.form['subject'] + '\n'
    #     msg = Message('Message from \'Contact Us Page\'', sender= 'info.reportthatpantry@gmail.com', 
    #     recipients=['info.reportthatpantry@gmail.com'], body = bodyText)
    #     mail.send(msg)
    #     return redirect(url_for('views.contact_us'))

    
    db.init_app(app)
    migrate.init_app(app, db)
    admin.init_app(app)
    mail.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import Student

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return Student.query.get(int(id))

    return app


def create_database(app):
    # if not path.exists('website/' + DB_NAME):
    db.create_all(app=app)
    print('Created Database!')


# gets the google provider configurations (the url for the authorization page on Google)
def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()