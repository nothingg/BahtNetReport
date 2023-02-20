from website import app
from flask import render_template, Blueprint, request, redirect, url_for, flash
from website.models import Reports, Branch , Banks
from website import db
from datetime import datetime, time
from sqlalchemy.exc import IntegrityError
from sqlalchemy import text

import os
import pandas as pd
import pytz
import ast

routes = Blueprint('routes', __name__)
timezone = pytz.timezone("Asia/Bangkok")
current_time = datetime.now(timezone)



@routes.route('/', methods=['GET', 'POST'])
def list_data():
    # items = Reports.query.order_by(Reports.cs_ref.desc()).all()
    # items = db.session.query(Reports ,Branch).join(Branch, Reports.dept == Branch.branch_id).all()

    date_format = '%Y-%m-%d'
    report_date = datetime.now().strftime(date_format)
    print('rpt date : ' + report_date)
    if request.method == 'POST':
        report_date = request.form['report_date']

    branch = Branch.query.order_by(Branch.branch_id).all()
    items = db.session.query(Reports, Branch).outerjoin(Branch, Reports.dept == Branch.branch_id)\
                        .filter(Reports.report_date == report_date)\
                        .order_by(Reports.report_time.asc()).all()

    # result = db.session.execute("SELECT * FROM my_model WHERE value < :value", {'value': 5.0})
    dr_normal = db.session.execute(text("select trim(TO_CHAR(count(*) , 'FM999,999,999,999'))  as dr_count  , " \
                                        "trim(TO_CHAR(sum(dr_amt) , '999,999,999,999.99'))  as dr_sum "\
                                        "from  public.reports a " \
                                        "where ( dept not in ('88828','999999','999998','999997') or dept is null ) and  dr_bic = 'GOHUTHB1' " \
                                        "and report_date = '" + report_date+"'")).fetchone()

    dr_nitikum = db.session.execute(text("select trim(TO_CHAR(count(*) , 'FM999,999,999,999'))  as dr_count  , " \
                                        "trim(TO_CHAR(sum(dr_amt) , '999,999,999,999.99'))  as dr_sum " \
                                        "from  public.reports a " \
                                        "where dept = '999999' and  dr_bic = 'GOHUTHB1' and report_date = '" + report_date + "'")).fetchone()

    cr_normal = db.session.execute(text("select trim(TO_CHAR(count(*) , 'FM999,999,999,999'))  as cr_count  , " \
                                         "trim(TO_CHAR(sum(cr_amt) , '999,999,999,999.99'))  as cr_sum " \
                                         "from  public.reports a " \
                                         "where  dr_bic != 'GOHUTHB1' and report_date = '" + report_date + "'")).fetchone()

    return render_template('list_data_orm.html', data=items, branches=branch , report_date = report_date , dr_normal = dr_normal , dr_nitikum = dr_nitikum , cr_normal = cr_normal)

@routes.route('/niti', methods=['GET', 'POST'])
def list_niti():
    date_format = '%Y-%m-%d'
    report_date = datetime.now().strftime(date_format)
    print('rpt date : ' + report_date)
    if request.method == 'POST':
        report_date = request.form['report_date']

    branch = Branch.query.order_by(Branch.branch_id).all()
    items = db.session.query(Reports, Branch).outerjoin(Branch, Reports.dept == Branch.branch_id) \
        .filter(Reports.report_date == report_date) \
        .filter(Reports.dept == '999999').filter(Reports.dr_bic == 'GOHUTHB1') \
        .order_by(Reports.report_time.asc()).all()

    dr_nitikum = db.session.execute(text("select trim(TO_CHAR(count(*) , 'FM999,999,999,999'))  as dr_count  , " \
                                         "trim(TO_CHAR(sum(dr_amt) , '999,999,999,999.99'))  as dr_sum " \
                                         "from  public.reports a " \
                                         "where dept = '999999' and  dr_bic = 'GOHUTHB1' and report_date = '" + report_date + "'")).fetchone()

    return render_template('list_niti.html', data=items, branches=branch , report_date = report_date , dr_nitikum = dr_nitikum )

@routes.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file_upload']
        report_date = request.form['report_date']

        if file and file.filename != '':
            data = pd.read_csv(file, skiprows=17)

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
            data['dr_amt'] = data['dr_amt'].str.replace(",", "").astype(float) if data[
                'dr_amt'].notnull().values.any() else 0
            data['cr_amt'] = data['cr_amt'].str.replace(",", "").astype(float) if data[
                'cr_amt'].notnull().values.any() else 0

            # covert Time
            # replace '.' with ':'
            data['column_to_convert'] = data['time'].str.replace('.', ':')

            # convert string to time
            data['report_time'] = pd.to_datetime(data['column_to_convert'], format='%H:%M:%S').dt.time

            # delete the column_to_convert column
            data = data.drop(['column_to_convert'], axis=1)

            data['created_date'] = current_time
            data['input_type'] = 'upload'
            data = data.fillna('')

            for index, row in data.iterrows():
                try:
                    row['amlo_is'] = False
                    if row['cr_bic'] == 'GOHUTHB1' and row['creditor_acct'] != '0010007369'and row['cr_amt'] >= 700000 :
                        row['amlo_is'] = True

                    model = Reports(cs_ref=row['cs_ref'],
                                    instruction_id=row['instruction_id'],
                                    mt=row['mt'],
                                    ctgypurp=row['ctgypurp'],
                                    dr_bic=row['dr_bic'],
                                    dr_acct=row['dr_acct'],
                                    cr_bic=row['cr_bic'],
                                    cr_acct=row['cr_acct'],
                                    # dr_amt=float(row['dr_amt']) if row['dr_amt'] else None,
                                    # cr_amt=float(row['cr_amt']) if row['cr_amt'] else None,
                                    dr_amt=row['dr_amt'],
                                    cr_amt=row['cr_amt'],
                                    status=row['status'],
                                    error=row['error'],
                                    time=row['time'],
                                    ch=row['ch'],
                                    transmission_type=row['transmission_type'],
                                    debtor_acct=row['debtor_acct'],
                                    debtor_name=row['debtor_name'],
                                    creditor_acct=row['creditor_acct'],
                                    creditor_name=row['creditor_name'],
                                    report_date=report_date,
                                    report_time=row['report_time'],
                                    created_date=row['created_date'],
                                    input_type=row['input_type'],
                                    amlo_is=row['amlo_is'], amlo_done=False ,
                                    dept = '999999' if 'GHB/UPD' in  row['instruction_id'] else None ,
                                    dr_bank = get_bank_short(row['dr_bic']) ,
                                    cr_bank = get_bank_short(row['cr_bic'])
                                    )
                    db.session.add(model)
                    db.session.commit()
                except IntegrityError:
                    db.session.rollback()

            flash('Upload successful!', category='success')
        else:
            flash('Upload Fail', category='error')

    return render_template('upload_transfer.html')

def get_bank_short(bank_bic):
    banks = Banks.query.filter(Banks.bank_bic == bank_bic ).first()
    rs = banks.bank_short if banks else None
    return rs

@routes.route('/form_insert')
def form_insert():
    return render_template('form_insert.html')


@routes.route('/insert', methods=['GET', 'POST'])
def insert():
    if request.method == 'POST':
        report = Reports(
            cs_ref=request.form['cs_ref'],
            instruction_id=request.form['instruction_id'],
            mt=request.form['mt'],
            ctgypurp=request.form['ctgypurp'],
            dr_bic=request.form['dr_bic'],
            dr_acct=request.form['dr_acct'],
            cr_bic=request.form['cr_bic'],
            cr_acct=request.form['cr_acct'],
            dr_amt=float(request.form['dr_amt']) if request.form['dr_amt'] else None,
            cr_amt=float(request.form['cr_amt']) if request.form['cr_amt'] else None,
            status=request.form['status'],
            error=request.form['error'],
            report_time=request.form['report_time'],
            ch=request.form['ch'],
            transmission_type=request.form['transmission_type'],
            debtor_acct=request.form['debtor_acct'],
            debtor_name=request.form['debtor_name'],
            creditor_acct=request.form['creditor_acct'],
            creditor_name=request.form['creditor_name'],
            dept=request.form['dept'],
            report_date=request.form['report_date'],
            created_date=current_time,
            input_type='input'
        )
        db.session.add(report)
        db.session.commit()

        return redirect(url_for('routes.list_data'))


@routes.route('/form_update/<string:id_data>')
def form_update(id_data):
    item = Reports.query.get(id_data)
    return render_template('form_update.html', data=item)


@routes.route('update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        item = Reports.query.get(request.form['cs_ref'])
        branch = Branch.query.filter(Branch.branch_name == request.form['branch-show']).first()
        item.dept = branch.branch_id
        # item.dept = request.form['dept']
        item.amlo_is = ast.literal_eval(request.form['amlo_is'])
        item.amlo_done = ast.literal_eval(request.form['amlo_done'])

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

@routes.route('/delete_date' , methods=['GET', 'POST'])
def delete_by_date():
    if request.method == 'POST':
        date_data = request.form['report_date']
        Reports.query.filter(Reports.report_date == date_data).delete(synchronize_session=False)

        db.session.commit()
        flash('Delete successful!', category='success')

    return render_template('delete_date.html')

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
