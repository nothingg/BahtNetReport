import pandas as pd
from sqlalchemy import create_engine

# create a connection to the database
engine = create_engine('postgresql://postgres:password@localhost:5432/postgres')

df = pd.read_csv('FundsTransfer170120231537.csv' , skiprows= 17)

# change the header of the dataframe
df = df.rename(columns={'CS Ref.': 'cs_ref',
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
df['instruction_id'] = df['instruction_id'].str.replace("^'", "", regex=True)
df['debtor_acct'] = df['debtor_acct'].str.replace("^'", "", regex=True)
df['creditor_acct'] = df['creditor_acct'].str.replace("^'", "", regex=True)

# check if there are any non-null values in a column
if df['dr_amt'].notnull().values.any():
    df['dr_amt'] = df['dr_amt'].str.replace(",", "").astype(float)

if df['cr_amt'].notnull().values.any():
        df['cr_amt'] = df['dr_amt'].str.replace(",", "").astype(float)


df.to_sql('reports', engine, if_exists='append', index=False)