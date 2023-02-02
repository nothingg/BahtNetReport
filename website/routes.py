from website import app
from flask import render_template , Blueprint
from website.models import Reports

routes = Blueprint('routes',__name__)

@routes.route('/')
def list_data():

     items = Reports.query.all()
     return render_template('list_data_orm.html',data = items)