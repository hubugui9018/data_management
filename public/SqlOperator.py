# -*-coding:utf-8 -*-
import pymysql
from django.db import connections
from sqlalchemy import create_engine
import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv)

class SqlOperator:
    def __init__(self):
        self.conn = None
        self.cursor = None

    def search(self, strsql):
        if 'select' in strsql.lower() and self.cursor != None:
            self.cursor.execute(strsql)
            data = self.cursor.fetchall()
            return data
        return None

    def insertMany(self, strsql, data):
        try:
            self.cursor.executemany(strsql, data)
            self.conn.commit()
        except Exception as e:
            print('执行Mysql: %s时出错： %s' % (strsql, e))
            self.conn.rollback()

    def insertOne(self, strsql, data):
        try:
            self.cursor.execute(strsql, data)
            self.conn.commit()
        except Exception as e:
            print('执行Mysql: %s时出错： %s' % (strsql, e))
            self.conn.rollback()

    def update(self, strsql, data):
        try:
            self.cursor.execute(strsql, data)
            self.conn.commit()
        except Exception as e:
            print('执行Mysql: %s时出错： %s' % (strsql, e))
            self.conn.rollback()

    def closeConn(self):
        pass
        # self.conn.close()

    def jcengine(self):
        engine = create_engine('mysql+pymysql://root:123456@192.168.70.151:3306/jcdata')
        with engine.connect() as conn, conn.begin():
            all_data_set = pd.read_sql_query('SELECT * FROM vsteaminfo', conn)
        return all_data_set