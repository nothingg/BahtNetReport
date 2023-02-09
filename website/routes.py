from website import app
from flask import render_template, Blueprint, request, redirect, url_for , flash
from website.models import Reports
from website import db
from datetime import datetime, time

import os
import pandas as pd
import pytz

routes = Blueprint('routes',__name__)
timezone = pytz.timezone("Asia/Bangkok")
current_time = datetime.now(timezone)



@routes.route('/')
def list_data():

    items = Reports.query.order_by(Reports.cs_ref.desc()).all()
    #items = db.session.execute(db.select(Reports)).fetchall()
    #items = db.session.query(Reports).all()
    # items = db.session.scalar(select(Reports)).all()
    return render_template('list_data_orm.html',data = items)

@routes.route('/upload' , methods=['GET','POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file_upload']

        if file and file.filename != '' :
            data = pd.read_csv(file, skiprows= 17)
            # change the header of the dataframe
            data = data.rename(columns={'CS Ref.': 'cs_ref',
                                    'Instruction ID': 'instruction_id',
                                    'MT': 'mt',
                                    'CtgyPurp': 'ctgypurp',
                                    'Dr BIC': 'dr_bic',
                                    'Dr Acc': 'dr_acct',
                                    'Cr BIC': 'cr_bic',
                                    'Cr Acc': 'cr_acct',
                                    'Dr Amt': 'dr_amt',
                                    'Cr Amt': 'cr_amt',
                                    'Status': 'status',
                                    'Error': 'error',
                                    'Time': 'time',
                                    'CH': 'ch',
                                    'Transmission Type': 'transmission_type',
                                    'Debtor Acc': 'debtor_acct',
                                    'Debtor Name': 'debtor_name',
                                    'Creditor Acc': 'creditor_acct',
                                    'Creditor Name': 'creditor_name'})

            # remove single quotes from the first position of a column
            data['instruction_id'] = data['instruction_id'].str.replace("^'", "", regex=True)
            data['debtor_acct'] = data['debtor_acct'].str.replace("^'", "", regex=True)
            data['creditor_acct'] = data['creditor_acct'].str.replace("^'", "", regex=True)

            # check if there are any non-null values in a column
            if data['dr_amt'].notnull().values.any():
                data['dr_amt'] = data['dr_amt'].str.replace(",", "").astype(float)

            if data['cr_amt'].notnull().values.any():
                data['cr_amt'] = data['dr_amt'].str.replace(",", "").astype(float)

            # covert Time
            # replace '.' with ':'
            data['column_to_convert'] = data['time'].str.replace('.', ':')

            # convert string to time
            data['report_time'] = pd.to_datetime(data['column_to_convert'], format='%H:%M:%S').dt.time

            # delete the column_to_convert column
            data = data.drop(['column_to_convert'], axis=1)

            data['created_date'] = current_time
            data['input_type'] = 'upload'

            # Connect to your database using the SQLAlchemy engine
            engine = db.engine

            # Insert the data into the PostgreSQL database
            data.to_sql('reports', engine, if_exists='append', index=False)

            flash('Upload successful!', category='success')
        else:
            flash('Upload Fail', category='error')

    return render_template('upload_transfer.html')

@routes.route('/form_insert')
def form_insert():

     return render_template('form_insert.html')

@routes.route('/insert', methods=['GET','POST'])
def insert():
    if request.method == 'POST':


        report = Reports(
            cs_ref = request.form['cs_ref'],
            instruction_id = request.form['instruction_id'],
            mt = request.form['mt'],
            ctgypurp = request.form['ctgypurp'],
            dr_bic = request.form['dr_bic'],
            dr_acct = request.form['dr_acct'],
            cr_bic = request.form['cr_bic'],
            cr_acct = request.form['cr_acct'],
            dr_amt = float(request.form['dr_amt'])  if request.form['dr_amt'] else None ,
            cr_amt = float(request.form['cr_amt']) if request.form['cr_amt'] else None ,
            status = request.form['status'],
            error = request.form['error'],
            report_time = request.form['report_time'],
            ch = request.form['ch'],
            transmission_type = request.form['transmission_type'],
            debtor_acct = request.form['debtor_acct'],
            debtor_name = request.form['debtor_name'],
            creditor_acct = request.form['creditor_acct'],
            creditor_name = request.form['creditor_name'],
            dept = request.form['dept'],
            report_date = request.form['report_date'],
            created_date = current_time,
            input_type = 'input'
        )
        db.session.add(report)
        db.session.commit()

        return redirect(url_for('routes.list_data'))

@routes.route('/form_update/<string:id_data>')
def form_update(id_data):
     item = Reports.query.get(id_data)
     return render_template('form_update.html', data=item)

@routes.route('update' , methods=['GET','POST'])
def update():
    if request.method == 'POST':
        item = Reports.query.get(request.form['cs_ref'])
        # print(item)
        item.instruction_id = request.form['instruction_id']
        item.mt = request.form['mt']
        item.ctgypurp = request.form['ctgypurp']
        item.dr_bic = request.form['dr_bic']
        item.dr_acct = request.form['dr_acct']
        item.cr_bic = request.form['cr_bic']
        item.cr_acct = request.form['cr_acct']
        item.dr_amt = request.form['dr_amt']
        item.cr_amt = request.form['cr_amt']
        item.status = request.form['status']
        item.error = request.form['error']
        item.time = request.form['time']
        item.ch = request.form['ch']
        item.transmission_type = request.form['transmission_type']
        item.debtor_acct = request.form['debtor_acct']
        item.debtor_name = request.form['debtor_name']
        item.creditor_acct = request.form['creditor_acct']
        item.creditor_name = request.form['creditor_name']
        item.dept = request.form['dept']
        # item. = request.form['']

        db.session.commit()

        flash('Update successful!', category='success')

        return redirect(url_for('routes.list_data'))

@routes.route('/delete/<string:id_data>')
def delete(id_data):
    item = Reports.query.get('id_data')
    db.session.delete(item)
    db.session.commit()

    flash('Delete successful!', category='success')
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
