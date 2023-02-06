from website import app
from flask import render_template, Blueprint, request, redirect, url_for
from website.models import Reports
from website import db

routes = Blueprint('routes',__name__)


@routes.route('/')
def list_data():
    items = Reports.query.order_by(Reports.cs_ref.desc()).all()
    #items = db.session.execute(db.select(Reports)).fetchall()
    #items = db.session.query(Reports).all()
    # items = db.session.scalar(select(Reports)).all()
    return render_template('list_data_orm.html',data = items)


@routes.route('/form_page/<string:id_data>')
def form_page(id_data):

     item = Reports.query.get(id_data)
     return render_template('form_page.html', data=item)

@routes.route('update' , methods=['GET','POST'])
def update():
    if request.method == 'POST':
        item = Reports.query.get(request.form['cs_ref'])
        item.debtor_name = request.form['debtor_name']
        item.creditor_name = request.form['creditor_name']

        db.session.commit()
        return redirect(url_for('routes.list_data'))

# @routes.route('/edit' , methods=['GET', 'POST'])
# def edit_data():
#
#      if request.method == 'POST':
#           item = Reports.query.get(request.form['cs_ref'])
#
#           # request.form['']
#           item.debtor_name = request.form['debtor_name']
#           item.creditor_name = request.form['creditor_name']
#
#           db.session.commit()
#           return redirect(url_for('routes.list_data'))
#
