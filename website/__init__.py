from flask import Flask
from os import path


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    # app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

    from .views import views


    app.register_blueprint(views, url_prefix='/')


    return app