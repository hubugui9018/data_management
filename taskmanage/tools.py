# -*- coding: utf-8 -*-

import collections
import datetime
import json
import os
import pickle
import random
import re
import time

import requests
import pymysql
from django.db import close_old_connections, transaction
# from django_redis import get_redis_connection


from auto_ui import settings
from public.SqlOperator import SqlOperator
from taskmanage.models import Task


class tools:
    _url = 'http://localhost:6800/{0}'

    # 关闭异常爬虫
    @classmethod
    def _cancelJobs(cls, type):
        resjobs = requests.get(cls._url.format('listjobs.json?project=zixun'))
        jsonjobs = json.loads(resjobs.text)
        for d in jsonjobs[type]:
            data = {'project': 'zixun', 'job': d['id']}
            res = requests.post(cls._url.format('cancel.json'), data=data)
            if 'ok' in res.text:
                continue

    # 调用爬虫
    @classmethod
    def _spiderszixun(cls, orglist):
        spidername = []

        surl = cls._url.format('schedule.json')
        lurl = cls._url.format('daemonstatus.json')
        for name in orglist:
            data = {'project': 'zixun', 'spider': name}
            try:
                res = requests.post(surl, data=data)
            except Exception as e:
                break
            txjson = json.loads(res.text)
            if txjson['status'] != 'ok':
                spidername.append(name)
        stime = datetime.datetime.today()
        while True:
            res = requests.get(lurl)
            lrejson = json.loads(res.text)
            if lrejson['running'] == 0:
                if lrejson['pending'] == 0:
                    break
                else:
                    cls._cancelJobs('pending')
                    continue
            else:
                time.sleep(60)
                tdelta = datetime.datetime.today() - stime
                if (50 * 60) < tdelta.total_seconds():
                    cls._cancelJobs('running')
        return spidername

    # 解析定时任务的参数数据
    @classmethod
    def _taskparamprase(cls, taskid):
        close_old_connections()
        try:
            Task.objects.filter(id=taskid).update(taskResult='进行中', modytime=datetime.datetime.today())
        except Exception as e:
            Task.objects.filter(id=taskid).update(taskResult='进行中', modytime=datetime.datetime.today())
        funparam = Task.objects.values('funcparam').filter(id=taskid)
        close_old_connections()

        ff = funparam[0]['funcparam'].split('|')

        if len(ff) == 1:
            cixing = ff[0]
            s = ''
        else:
            cixing = ff[0]
            s = ff[1]

        t = datetime.date.today()  # date类型
        dt = datetime.datetime.strptime(str(t), '%Y-%m-%d')  # date转str再转datetime

        if s == '':
            sdate = ''
        else:
            if int(s) == 0:
                sdate = ''
            else:
                sdate = dt - abs(datetime.timedelta(days=int(s)))
        return cixing, sdate

    # 调用球队资讯-英超
    @classmethod
    def teamzixunall(cls, taskid):

        sdate = cls._taskparamprase(taskid)

        db_config = {
            'host': '192.168.70.151',
            'user': 'root',
            'password': '123456',
            'database': 'jcdata'
        }

        osql = NewSqlOperator(db_config)
        osql.connect()

        teamlist = osql.search(
            "SELECT spider_name FROM `teaminfo` WHERE `liansai` = '英超' AND `spider_name` IS NOT NULL LIMIT 0, 1000")
        osql.closeConn()

        teamname = []
        teamname.extend([team[0] for team in teamlist])
        spideranmel = cls._spiderszixun(teamname)
        if len(spideranmel) > 0:
            cls._spiderszixun(spideranmel)


class NewSqlOperator:
    def __init__(self, db_config):
        self.db_config = db_config
        self.connection = None

    def connect(self):
        try:
            self.connection = pymysql.connect(
                host=self.db_config['host'],
                user=self.db_config['user'],
                password=self.db_config['password'],
                database=self.db_config['database']
            )

        except pymysql.MySQLError as e:
            print(f"Error connecting to database: {e}")
            raise

    def closeConn(self):
        if self.connection:
            self.connection.close()

    def search(self, query):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()
                return result
        except pymysql.MySQLError as e:
            print(f"Error executing query: {e}")
            raise
