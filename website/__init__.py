from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SECRET_KEY'] = 'Hello Flask for Bahtnet report'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost:5432/postgres'

db = SQLAlchemy(app)

from website.routes import routes
app.register_blueprint(routes, url_prefix='/')


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