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


for index, row in df.iterrows():
    print(row['instruction_id'])