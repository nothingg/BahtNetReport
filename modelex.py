from sqlalchemy import create_engine, Column, Integer, String

from sqlalchemy.orm import sessionmaker
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Report(Base):
    __tablename__ = 'reports'
    # id = Column(Integer, primary_key=True)
    cs_ref = Column(String, primary_key=True)
    instruction_id = Column(String)
    mt = Column(String)
    ctgypurp = Column(String)
    dr_bic = Column(String)
    dr_acct = Column(String)
    cr_bic = Column(String)
    cr_acct = Column(String)
    dr_amt = Column(String)
    cr_amt = Column(String)
    status = Column(String)
    error = Column(String)
    time = Column(String)
    ch = Column(String)
    transmission_type = Column(String)
    debtor_acct = Column(String)
    debtor_name = Column(String)
    creditor_acct = Column(String)
    creditor_name = Column(String)
    dept = Column(String)

# create a connection to the database
engine = create_engine('postgresql://postgres:password@localhost:5432/postgres')
Base.metadata.create_all(engine)


Session = sessionmaker(bind=engine)
session = Session()

result = session.query(Report).filter(Report.cs_ref == "230117017680").all()
for report in result:
    print(report.cs_ref, report.instruction_id ,report.time )
