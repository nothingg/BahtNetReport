from flask import Blueprint , render_template ,request , flash , jsonify , redirect , url_for
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



@views.route("/update",methods=['POST'])
def update():

    sql = "UPDATE reports SET  debtor_name = '"+  request.form['debtor_name']  +"' , creditor_name = '"+ request.form['creditor_name'] +"' WHERE cs_ref = '"+ request.form['cs_ref'] +"' "
    print(sql)

    # engine = create_engine("postgresql://user:password@localhost/dbname")
    # conn = engine.connect()
    #
    # query_string = "UPDATE users SET username='new_username' WHERE id=1"
    # conn.execute(query_string)
    #
    # engine.connect().execute(text(sql))

    with engine.connect().execution_options(autocommit=True) as conn:
        conn.execute(text(sql))
        conn.commit()

    return redirect(url_for('views.list_data'))
