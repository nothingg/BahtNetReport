from flask import Blueprint , render_template ,request , flash , jsonify

import pandas as pd
from sqlalchemy import create_engine

from sqlalchemy.sql import text


# create a connection to the database
engine = create_engine('postgresql://postgres:password@localhost:5432/postgres')

sql = '''
    SELECT * FROM reports;
'''
with engine.connect().execution_options(autocommit=True) as conn:
    query = conn.execute(text(sql))
df = pd.DataFrame(query.fetchall())

views = Blueprint('views',__name__)

@views.route('/')
def list_data():
    print(df)
    return render_template('list_data.html',data=df)