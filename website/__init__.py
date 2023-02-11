import logging
from flask import Flask , flash , redirect
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SECRET_KEY'] = 'Hello Flask for Bahtnet report'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost:5432/postgres'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

# logging.basicConfig()
# logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

from website.routes import routes

app.register_blueprint(routes, url_prefix='/')

# @app.errorhandler(Exception)
# def handle_exception(e):
#     flash("An error occurred: {}".format(e), category='error')
#     return redirect("/")


#
# def create_app():
#     app = Flask(__name__)
#     app.config['SECRET_KEY'] = 'Hello Flask for Bahtnet report'
#     app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost:5432/postgres'
#
#     from .views import views
#
#
#     app.register_blueprint(views, url_prefix='/')
#
#
#     return app