import logging
import pandas as pd
import numpy as np
import contextlib


from sqlalchemy import create_engine, and_
from sqlalchemy.orm import sessionmaker, Session, Query
from sqlalchemy.inspection import inspect


#######################################
###  Base Database Configuration    ###
#######################################

class baseDbInf:
    def __init__(self, driver: str):
        self.driver = driver

    def bindServer(self, ip: str, port: int, db: str):
        self.ip = ip
        self.port = port
        self.db = db

    def login(self, username: str, password: str):
        self.username = username
        self.password = password

    def argTempStr(self):
        raise NotImplementedError("Must implement this method to get different arg placeholder for different database")

    def getConnStr(self) -> str:
        #engine = create_engine('mysql+mysqlconnector://USRNAME:PSWD@localhost:3306/DATABASE?charset=ytf8')
        #engine = create_engine("ibm_db_sa://USRNAME:PSWD@IP:PORT/DATABASE?charset=utf8")
        #engine = create_engine('sqlite:///DB_ADDRESS')
        return f"{self.driver}://{self.username}:{self.password}@{self.ip}:{self.port}/{self.db}?charset=utf8"

    def launch(self):
        connStr = self.getConnStr()
        self.engine = create_engine(connStr)
        self.DBSession = sessionmaker(bind = self.engine)
        logging.info("Engine started, ready to go!")

    def newSession(self):
        try:
            session = self.DBSession()
        except Exception as e:
            logging.error(e)
        else:
            return session

    def getJdbcUrl(self) -> str:
        # for spark connection and other purpose
        raise NotImplementedError("Must implement this method to get different JdbcUrl for different database")

    def getDriverClass(self) -> str:
        # for spark connection and other purpose
        raise NotImplementedError("Must implement this method to get different DriverClass for different database")


#############################################
### Provider level database Configuration ###
#############################################

class MySQL(baseDbInf):
    def __init__(self, driver = "mysqlconnector"):
        super().__init__(f"mysql+{driver}")

    def argTempStr(self):
        return "%s"

    def getJdbcUrl(self) -> str:
        return f"jdbc:mysql://{self.ip}:{self.port}/{self.db}"

    def getDriverClass(self) -> str:
        # https://repo1.maven.org/maven2/mysql/mysql-connector-java/8.0.27/mysql-connector-java-8.0.27.jar
        return "com.mysql.jdbc.Driver"

class DB2(baseDbInf):
    def __init__(self):
        super().__init__("ibm_db_sa")

    def argTempStr(self):
        return "?"

    def getJdbcUrl(self) -> str:
        return f"jdbc:db2://{self.ip}:{self.port}/{self.db}"

    def getDriverClass(self) -> str:
        # https://repo1.maven.org/maven2/com/ibm/db2/jcc/db2jcc/db2jcc4/db2jcc-db2jcc4.jar
        return "com.ibm.db2.jcc.DB2Driver"

class SqLite(baseDbInf):
    def __init__(self, dburl):
        super().__init__("sqlite")
        self.dburl = dburl

    def getConnStr(self) -> str:
        return f"sqlite:///{self.dburl}"

    def argTempStr(self):
        return "?"

    def getJdbcUrl(self) -> str:
        return f"jdbc:sqlite://{self.dburl}"

    def getDriverClass(self) -> str:
        # https://repo1.maven.org/maven2/org/xerial/sqlite-jdbc/3.36.0.3/sqlite-jdbc-3.36.0.3.jar
        return "org.sqlite.JDBC"

class SqlServer(baseDbInf):
    def __init__(self):
        super().__init__("mssql+pymssql")

    def argTempStr(self):
        return "?"

    def getJdbcUrl(self) -> str:
        return f"jdbc:sqlserver://{self.ip}:{self.port}/{self.db}"

    def getDriverClass(self) -> str:
        # https://repo1.maven.org/maven2/com/microsoft/sqlserver/mssql-jdbc/8.4.0.jre8/mssql-jdbc-8.4.0.jre8.jar
        return "com.microsoft.sqlserver.jdbc.SQLServerDriver"

class Oracle(baseDbInf):
    def __init__(self, sid: str):
        super().__init__("oracle")
        self.sid = sid

    def argTempStr(self):
        return "?"

    def getJdbcUrl(self) -> str:
        return f"jdbc:oracle:thin:/@(DESCRIPTION=(ADDRESS=(PROTOCOL=tcp)(HOST={self.ip})(PORT={self.port}))(CONNECT_DATA=(SID={self.sid})))"

    def getDriverClass(self) -> str:
        # https://repo1.maven.org/maven2/com/oracle/database/jdbc/ojdbc8/19.3.0.0/ojdbc8-19.3.0.0.jar
        return "oracle.jdbc.driver.OracleDriver"

class PostgreSql(baseDbInf):
    def __init__(self):
        super().__init__("postgresql+psycopg2")

    def argTempStr(self):
        return "?"

    def getJdbcUrl(self) -> str:
        return f"jdbc:postgresql://{self.ip}:{self.port}/{self.db}"

    def getDriverClass(self) -> str:
        # https://repo1.maven.org/maven2/org/postgresql/postgresql/42.2.18/postgresql-42.2.18.jar
        return "org.postgresql.Driver"