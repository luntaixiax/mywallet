from datetime import date
from sqlalchemy import func, distinct, and_
from sqlalchemy_utils import Currency
import logging

from walletServer.models.constants import CategType, AcctType
from walletServer.models.tables import User, Categ, Acct
from walletServer.utils.querier import dba
from walletServer.utils.tools import id_generator


class userDao:

    @ classmethod
    def register(cls, username: str, password: str, dob: date, email: str, phone: str) -> int:

        with dba.get_session() as s:
            q = s.query(func.count(User.username)).filter(User.username == username).scalar()
            if q == 0:
                user_id = id_generator(prefix = "u-")
                s.add(User(user_id = user_id, username = username, password = password,
                           dob = dob, email = email, phone = phone))
                logging.info(f"Successfully registered user: {username}")
                return 1
            else:
                logging.error(f"User already exists: {username}")
                return 0

    @ classmethod
    def delete(cls, username: str) -> int:

        with dba.get_session() as s:
            user_id = s.query(User.user_id).filter(User.username == username).scalar()
            if user_id:
                s.query(User).filter(User.user_id == user_id).delete()
                logging.info(f"Successfully delete user: {username}, userid: {user_id}")
                return 1
            else:
                logging.error(f"User not found")
                return 0

    @ classmethod
    def validate(cls, username: str, password: str) -> 1:
        with dba.get_session() as s:
            user = s.query(User).filter(User.username == username).one()
            return int(user.password == password)  # 1/0

    @ classmethod
    def update_profile(cls, username: str, **kws):
        p = {"username": username}  # use to find which records to update_all
        dba.update(User, p, kws)

    @ classmethod
    def get_userid(cls, username: str) -> str:
        with dba.get_session() as s:
            return s.query(User.user_id).filter(User.username == username).scalar()


class categDao:
    def __init__(self, username: str):
        self.username = username
        self.user_id = userDao.get_userid(username)

    def add(self, categ_name: str, categ_type: CategType):
        with dba.get_session() as s:
            q = s.query(func.count(Categ.categ_id)).filter(and_(Categ.user_id == self.user_id, Categ.categ_name == categ_name)).scalar()
            if q == 0:
                categ_id = id_generator(prefix = "c-")
                s.add(Categ(user_id = self.user_id, categ_id = categ_id,
                            categ_name = categ_name, categ_type = categ_type))
                logging.info(f"Successfully added categ: {categ_name} for user {self.username}")
                return 1
            else:
                logging.error(f"Categ {categ_name} already exists for user {self.username}")
                return 0

class acctDao:
    def __init__(self, username: str):
        self.username = username
        self.user_id = userDao.get_userid(username)

    def add(self, acct_name: str, acct_type: AcctType, cur: str):
        with dba.get_session() as s:
            q = s.query(func.count(Acct.acct_id)).filter(and_(Acct.user_id == self.user_id, Acct.acct_name == acct_name)).scalar()
            if q == 0:
                acct_id = id_generator(prefix = "a-")
                s.add(Acct(user_id = self.user_id, acct_id = acct_id,
                            acct_name = acct_name, acct_type = acct_type, cur = Currency(cur)))
                logging.info(f"Successfully added categ: {acct_name} for user {self.username}")
                return 1
            else:
                logging.error(f"Account {acct_name} already exists for user {self.username}")
                return 0

if __name__ == '__main__':
    #userDao.register(username = 'luntaixia', password = 'allan19950601', dob = date(1995, 6, 1), email = 'ailunqian124@gmail.com', phone = '226-978-7365')
    #userDao.register(username='evelyn', password='123456', dob = date(1997, 6, 12), email='evelyn@gmail.com', phone='123-456-7890')
    #userDao.update_profile(username='allan', password='luntai', email='2371335097@qq.com')
    #userDao.delete('luntaixia')
    #print(userDao.validate('allan', 'luntai'))
    cd = acctDao('luntaixia')

    cd.add('Cash(CNY)', AcctType.ASSET, 'CNY')
    cd.add('Cash(CAD)', AcctType.ASSET, 'CAD')
    cd.add('Cash(USD)', AcctType.ASSET, 'USD')
    cd.add('Cash(HKD)', AcctType.ASSET, 'HKD')
    cd.add('Cash(MOP)', AcctType.ASSET, 'MOP')
    cd.add('Cash(GBP)', AcctType.ASSET, 'GBP')

    cd.add('BOC(CAD)', AcctType.ASSET, 'CAD')
    cd.add('BOC(EUR)', AcctType.ASSET, 'EUR')
    cd.add('CMBC(CAD)', AcctType.ASSET, 'CAD')

    cd.add('Wechat', AcctType.ASSET, 'CNY')
    cd.add('Alipay', AcctType.ASSET, 'CNY')
    cd.add('BOC(CNY)', AcctType.ASSET, 'CNY')
    cd.add('CMBC(CNY)', AcctType.ASSET, 'CNY')
    cd.add('CRB(CNY)', AcctType.ASSET, 'CNY')
    cd.add('ICBC(CNY)', AcctType.ASSET, 'CNY')
    cd.add('CCB(CNY)', AcctType.ASSET, 'CNY')

    cd.add('Ali Sav', AcctType.ASSET, 'CNY')
    cd.add('BOC Sav', AcctType.ASSET, 'CNY')
    cd.add('CMBC Sav', AcctType.ASSET, 'CNY')

    cd.add('TD Check', AcctType.ASSET, 'CAD')
    cd.add('TD US', AcctType.ASSET, 'USD')
    cd.add('BNS Check', AcctType.ASSET, 'CAD')
    cd.add('Tanger Check', AcctType.ASSET, 'CAD')

    cd.add('TD Sav', AcctType.ASSET, 'CAD')
    cd.add('BNS MPSA', AcctType.ASSET, 'CAD')
    cd.add('Tanger Sav', AcctType.ASSET, 'CAD')
    cd.add('GIC', AcctType.ASSET, 'CAD')

    cd.add('Ali MM', AcctType.ASSET, 'CNY')
    cd.add('BOC Treasury', AcctType.ASSET, 'CNY')
    cd.add('CMBC MM', AcctType.ASSET, 'CNY')

    cd.add('CRB MM', AcctType.ASSET, 'CNY')
    cd.add('CMBC Fund', AcctType.ASSET, 'CNY')
    cd.add('BOC Fund', AcctType.ASSET, 'CNY')

    cd.add('CMBC Fund(R)', AcctType.ASSET, 'CNY')
    cd.add('Ali Fund(R)', AcctType.ASSET, 'CNY')
    cd.add('Ali AI(R)', AcctType.ASSET, 'CNY')
    cd.add('CMBC OTC(R)', AcctType.ASSET, 'CNY')

    cd.add('IBRK', AcctType.ASSET, 'CAD')
    cd.add('WST-TFSA', AcctType.ASSET, 'CAD')
    cd.add('WST-PERS', AcctType.ASSET, 'CAD')
    cd.add('Div-Recv', AcctType.ASSET, 'CAD')
    cd.add('IP Cash', AcctType.ASSET, 'CAD')

    cd.add('Pestrol', AcctType.ASSET, 'CAD')
    cd.add('Prepaid', AcctType.ASSET, 'CAD')
    cd.add('Canteen', AcctType.ASSET, 'CNY')

    cd.add('RSP', AcctType.ASSET, 'CAD')
    cd.add('HBP', AcctType.ASSET, 'CNY')  # 住房公积金

    cd.add('Car', AcctType.ASSET, 'CAD')
    cd.add('Furniture', AcctType.ASSET, 'CAD')

    cd.add('Insur', AcctType.ASSET, 'CAD')
    cd.add('Receivable(CAD)', AcctType.ASSET, 'CAD')
    cd.add('Deposit(CAD)', AcctType.ASSET, 'CAD')
    cd.add('Prepaid(CAD)', AcctType.ASSET, 'CAD')
    cd.add('Rent Prepaid(CAD)', AcctType.ASSET, 'CAD')
    cd.add('Dianfu(CAD)', AcctType.ASSET, 'CAD')

    cd.add('TD Credit', AcctType.LIABILITY, 'CAD')
    cd.add('BNS Amex', AcctType.LIABILITY, 'CAD')
    cd.add('Amex', AcctType.LIABILITY, 'CAD')

    cd.add('CMBC Credit', AcctType.LIABILITY, 'CNY')
    cd.add('ICBC Credit', AcctType.LIABILITY, 'CNY')
    cd.add('Ant LoC', AcctType.LIABILITY, 'CNY')
    cd.add('JD LoC', AcctType.LIABILITY, 'CNY')

    cd.add('Rent Prepaid(CNY)', AcctType.LIABILITY, 'CNY')
    cd.add('Deposit(CNY)', AcctType.LIABILITY, 'CNY')
    cd.add('Receivable(CNY)', AcctType.LIABILITY, 'CNY')

    cd.add('Borrow(CNY)', AcctType.LIABILITY, 'CNY')
    cd.add('Family(CNY)', AcctType.LIABILITY, 'CNY')
    cd.add('Payable(CNY)', AcctType.LIABILITY, 'CNY')


    # cd.add('Rental', CategType.EXPENSE)
    # cd.add('Insurance', CategType.EXPENSE)
    # cd.add('Utility', CategType.EXPENSE)
    # cd.add('Mngmt', CategType.EXPENSE)
    # cd.add('Telecom', CategType.EXPENSE)
    # cd.add('Tax', CategType.EXPENSE)
    #
    # cd.add('Dine out', CategType.EXPENSE)
    # cd.add('Drinks', CategType.EXPENSE)
    # cd.add('Snacks', CategType.EXPENSE)
    # cd.add('Grocery', CategType.EXPENSE)
    #
    # cd.add('Appliance', CategType.EXPENSE)
    # cd.add('Furniture', CategType.EXPENSE)
    # cd.add('Households', CategType.EXPENSE)
    #
    # cd.add('Train', CategType.EXPENSE)
    # cd.add('Subway', CategType.EXPENSE)
    # cd.add('Gas', CategType.EXPENSE)
    # cd.add('Parking', CategType.EXPENSE)
    # cd.add('Bus', CategType.EXPENSE)
    # cd.add('Taxi', CategType.EXPENSE)
    # cd.add('Fight', CategType.EXPENSE)
    # cd.add('Ferry', CategType.EXPENSE)
    #
    # cd.add('Tuition', CategType.EXPENSE)
    # cd.add('Edu other', CategType.EXPENSE)
    #
    # cd.add('Apparel', CategType.EXPENSE)
    # cd.add('Drug', CategType.EXPENSE)
    # cd.add('Staple', CategType.EXPENSE)
    #
    # cd.add('Barber', CategType.EXPENSE)
    # cd.add('Movie', CategType.EXPENSE)
    # cd.add('Game', CategType.EXPENSE)
    # cd.add('Entertain', CategType.EXPENSE)
    # cd.add('Membership', CategType.EXPENSE)
    # cd.add('Agent', CategType.EXPENSE)
    # cd.add('Shipping', CategType.EXPENSE)
    #
    # cd.add('Treat', CategType.EXPENSE)
    # cd.add('Gift', CategType.EXPENSE)
    # cd.add('Redpack Out', CategType.EXPENSE)
    #
    # cd.add('Ticket', CategType.EXPENSE)
    # cd.add('Hotel', CategType.EXPENSE)
    # cd.add('Tourism', CategType.EXPENSE)
    #
    # cd.add('Trial Bal Out', CategType.EXPENSE)
    # cd.add('Unexpected Loss', CategType.EXPENSE)
    # cd.add('Unrealized Loss', CategType.EXPENSE)
    # cd.add('Realized Loss', CategType.EXPENSE)
    #
    # cd.add('Salary', CategType.INCOME)
    # cd.add('Subsidy', CategType.INCOME)
    # cd.add('Bonus', CategType.INCOME)
    # cd.add('Parttime', CategType.INCOME)
    #
    # cd.add('Reimburse', CategType.INCOME)
    # cd.add('Redpack In', CategType.INCOME)
    # cd.add('Benefit', CategType.INCOME)
    # cd.add('Tax Return', CategType.INCOME)
    #
    # cd.add('Trial Bal In', CategType.INCOME)
    # cd.add('Refund', CategType.INCOME)
    #
    # cd.add('Rental Inc', CategType.INCOME)
    # cd.add('Unrealized Gain', CategType.INCOME)
    # cd.add('Realized Gain', CategType.INCOME)
    #
    # cd.add('Pension(Per)', CategType.INCOME)
    # cd.add('Pension(Corp)', CategType.INCOME)