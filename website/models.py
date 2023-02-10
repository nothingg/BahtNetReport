from website import db
import datetime
import pytz

thailand_tz = pytz.timezone("Asia/Bangkok")

class Branch(db.Model):
    branch_id = db.Column(db.String, primary_key=True)
    branch_name = db.Column(db.String)
    branch_desc = db.Column(db.String)

# create the extension
class Reports(db.Model):
    # __tablename__ = 'reports'
    cs_ref = db.Column(db.String, primary_key=True)
    instruction_id = db.Column(db.String)
    mt = db.Column(db.String)
    ctgypurp = db.Column(db.String)
    dr_bic = db.Column(db.String)
    dr_acct = db.Column(db.String)
    cr_bic = db.Column(db.String)
    cr_acct = db.Column(db.String)
    dr_amt = db.Column(db.Integer)
    cr_amt = db.Column(db.Integer)
    status = db.Column(db.String)
    error = db.Column(db.String)
    ch = db.Column(db.String)
    transmission_type = db.Column(db.String)
    debtor_acct = db.Column(db.String)
    debtor_name = db.Column(db.String)
    creditor_acct = db.Column(db.String)
    creditor_name = db.Column(db.String)
    dept = db.Column(db.String)
    report_date = db.Column(db.Date)
    report_time = db.Column(db.Time)
    created_date = db.Column(db.DateTime , default=lambda : datetime.datetime.now(thailand_tz))
    input_type = db.Column(db.String)
    amlo_is = db.Column(db.Boolean)
    amlo_done = db.Column(db.Boolean)

    def __repr__(self):
        return "<Reports : "+ str(self.instruction_id)




# Base = declarative_base()
#
# class Reports(Base):
#     # __tablename__ = 'reports'
#     cs_ref = Column(String, primary_key=True)
#     instruction_id = Column(String)
#     mt = Column(String)
#     ctgypurp = Column(String)
#     dr_bic = Column(String)
#     dr_acct = Column(String)
#     cr_bic = Column(String)
#     cr_acct = Column(String)
#     dr_amt = Column(String)
#     cr_amt = Column(String)
#     status = Column(String)
#     error = Column(String)
#     time = Column(String)
#     ch = Column(String)
#     transmission_type = Column(String)
#     debtor_acct = Column(String)
#     debtor_name = Column(String)
#     creditor_acct = Column(String)
#     creditor_name = Column(String)
#     dept = Column(String)
#
#     def __repr__(self):
#         return '<Reports %r> ' % self.cs_ref