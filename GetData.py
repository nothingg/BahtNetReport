# import pandas as pd
# from sqlalchemy import create_engine
#
# from sqlalchemy.sql import text
#
# # create a connection to the database
# engine = create_engine('postgresql://postgres:password@localhost:5432/postgres')
#
# sql = '''
#     SELECT * FROM reports;
# '''
# with engine.connect().execution_options(autocommit=True) as conn:
#     query = conn.execute(text(sql))
# df = pd.DataFrame(query.fetchall())
#
#
# for index, row in df.iterrows():
#     print(row['instruction_id'])
#
#
data = ['cs_ref', 'instruction_id', 'mt', 'ctgypurp', 'dr_bic', 'dr_acct', 'cr_bic', 'cr_acct', 'dr_amt', 'cr_amt', 'status', 'error', 'time', 'ch', 'transmission_type', 'debtor_acct', 'debtor_name', 'creditor_acct', 'creditor_name', 'report_time', 'created_date', 'input_type']

for item in data:
    print(item + "=row['" + item + "'],")