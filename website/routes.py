from website import app
from flask import render_template, Blueprint, request, redirect, url_for
from website.models import Reports
from website import db

routes = Blueprint('routes',__name__)

@routes.route('/')
def list_data():
     items = Reports.query.all()
     return render_template('list_data_orm.html',data = items)


@routes.route("/edit_page/<string:id_data>/" , methods=['GET'])
def edit_page(id_data):

     item = Reports.query.get(id_data)
     return render_template('form_data.html', data=item)

@routes.route('/edit' , methods=['GET', 'POST'])
def edit_data():

     if request.method == 'POST':
          item = Reports.query.get(request.form['cs_ref'])

          # request.form['']
          item.debtor_name = request.form['debtor_name']
          item.creditor_name = request.form['creditor_name']

          db.session.commit()
          return redirect(url_for('routes.list_data'))

