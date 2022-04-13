from sqlalchemy.ext.declarative import declarative_base, as_declarative
from sqlalchemy import ForeignKey, UniqueConstraint, Column, Integer, String, Text, Date, DateTime, Float, Numeric, DECIMAL, inspect, INT
from sqlalchemy_utils import EmailType, PasswordType, PhoneNumberType, ChoiceType, CurrencyType, Currency

from walletServer.models.constants import AcctType, CategType, EntryType

Base = declarative_base()

class User(Base):
    __tablename__ = "user"

    user_id = Column(String(length = 10), primary_key = True, nullable = False)
    username = Column(String(length = 25), nullable = False, unique = True)
    password = Column(PasswordType(schemes=['pbkdf2_sha512','md5_crypt'], deprecated = ['md5_crypt']), nullable = False)
    dob = Column(Date, nullable = False)  # date of birth
    email = Column(EmailType, nullable = False)  # date of birth
    phone = Column(PhoneNumberType(region = 'US'), nullable = False)

class Acct(Base):
    __tablename__ = "acct"

    acct_id = Column(String(length = 10), primary_key = True, nullable = False)
    acct_name = Column(String(length = 25), nullable = False)
    user_id = Column(String(length = 10), ForeignKey('user.user_id', onupdate = 'CASCADE'), nullable = False)
    acct_type = Column(ChoiceType(AcctType, impl = Integer()), nullable = False)
    cur = Column(CurrencyType, nullable = False)

class Transaction(Base):
    __tablename__ = "transaction"

    trans_id = Column(String(length = 10), primary_key = True, nullable = False)
    trans_dt = Column(DateTime, nullable = True)
    user_id = Column(String(length = 10), ForeignKey('user.user_id', onupdate = 'CASCADE'), nullable = False)
    note = Column(Text, nullable = True)

class Categ(Base):
    __tablename__ = "categ"

    categ_id = Column(String(length = 10), primary_key = True, nullable = False)
    categ_name = Column(String(length = 25), nullable = False)
    user_id = Column(String(length = 10), ForeignKey('user.user_id', onupdate = 'CASCADE'), nullable = False)
    categ_type = Column(ChoiceType(CategType, impl = Integer()), nullable = False) # income/expense

class Entry(Base):
    __tablename__ = "entry"

    entry_id = Column(String(length = 10), primary_key = True, nullable = False)
    trans_id = Column(String(length = 10), ForeignKey('transaction.trans_id', ondelete = 'CASCADE' ,onupdate = 'CASCADE'), nullable = False)
    entry_type = Column(ChoiceType(EntryType, impl = Integer()), nullable = False) # debit/credit
    acct_id = Column(String(length = 10), ForeignKey('acct.acct_id', onupdate = 'CASCADE'), nullable = True) # account transfer case
    categ_id = Column(String(length = 10), ForeignKey('categ.categ_id', onupdate = 'CASCADE'), nullable = True) # income/expense case
    amount = Column(DECIMAL(15, 2), nullable = False, server_default = "0.0")
    project = Column(String(length = 10), nullable = True)  # daily/investment/other


if __name__ == '__main__':
    from walletServer.utils.dbconfigs import MySQL
    from walletServer.utils.dbapi import dbIO

    lm = MySQL()
    lm.bindServer('localhost', 3306, 'wallet')
    lm.login('root', 'allan19950601')
    lm.launch()

    #Base.metadata.create_all(lm.engine)

    db = dbIO(lm)

    #db.insert(User, dict(user_id = 'u001', username = 'luntaixia', password = 'allan19950601', dob = '1995-06-01', email = 'ailunqian124@gmail.com', phone = '226-978-7365'))
    #db.insert(User, dict(user_id='u002', username='evelyn', password='123456', dob='1997-06-12',
    #                     email='evelyn@gmail.com', phone='123-456-7890'))
    #db.insert(Acct, dict(acct_id = 'acct002', user_id = 'u001', acct_type = AcctType.ASSET, cur = Currency('CAD')))
    from sqlalchemy import func, distinct

    with db.get_session() as s:
        q = s.query(func.count(User.user_id)).filter(User.user_id == 'u003')
        #assert u.password == 'xxxx'

    print(q.scalar())  # Canadian Dollar