from flask import Blueprint , render_template ,request , flash , jsonify
from sqlalchemy import create_engine
from sqlalchemy.sql import text
import pandas as pd
import locale


# create a connection to the database
engine = create_engine('postgresql://postgres:password@localhost:5432/postgres')




views = Blueprint('views',__name__)

@views.route('/')
def list_data():
    sql = '''
        SELECT * FROM reports;
    '''
    with engine.connect().execution_options(autocommit=True) as conn:
        query = conn.execute(text(sql))
    df = pd.DataFrame(query.fetchall())

    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    df['dr_amt'] = df['dr_amt'].astype(float).apply(lambda x: locale.format("%.2f", x, grouping=True))
    df['cr_amt'] = df['cr_amt'].astype(float).apply(lambda x: locale.format("%.2f", x, grouping=True))

    return render_template('list_data.html',data=df)

@views.route("/edit/<string:id_data>",methods=['GET'])
def edit_data(id_data):
    sql = " SELECT * FROM reports WHERE cs_ref = '" + id_data + "'"

    with engine.connect().execution_options(autocommit=True) as conn:
        query = conn.execute(text(sql))
    df = pd.DataFrame(query.fetchall())

    df.loc[0]
    # df.head(1)


    return render_template('edit_data.html',data=df.loc[0])