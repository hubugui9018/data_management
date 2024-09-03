# -*- coding: utf-8 -*-

import logging
from datetime import datetime

from django.db import close_old_connections
from apscheduler.events import EVENT_JOB_ERROR, EVENT_JOB_MISSED, EVENT_JOB_EXECUTED
from apscheduler.executors.pool import ProcessPoolExecutor
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.background import BackgroundScheduler

# from auto_ui import settings
#
from taskmanage.models import Task
from taskmanage.tools import tools

logger = logging.getLogger('taskmanage')

class Job:


    def setparam(self, taskfun='',taskid='',sdate='',edate='', schedule='', taskType=''):
        self.taskfun = taskfun
        self.taskid = taskid
        self.schedule = schedule
        self.sdate = sdate
        self.taskType = taskType
        self.edate = edate


    # 把时间表做数据处理
    def __get_date(self):
        if self.taskType == 'cron':#year|month|day|week|day_of_week|hours|minutes|seconds
            cornstr = self.schedule.split('|')
            return {'year': cornstr[0],'month':cornstr[1],'day':cornstr[2],'week':cornstr[3],'dayofweek':cornstr[4],'hour':cornstr[5],'minutes':cornstr[6],'seconds':cornstr[7]}

        elif self.taskType == 'interval':  # 间隔执行 #week|days|hours|minutes|seconds
            intervalstr = self.schedule.split('|')
            return {'week':intervalstr[0],'day':intervalstr[1],'hour':intervalstr[2],'minutes':intervalstr[3],'seconds':intervalstr[4]}

    def setSchedule(self, type):
        jobStore = {
            'defualt': SQLAlchemyJobStore(url='sqlite:///jobs.sqlite')
        #     mysql+pymysql://username:password@127.0.0.1:3306/dbname?charset=utf8
        }
        executors = {
            # 'default': ThreadPoolExecutor,
            'processpool': ProcessPoolExecutor(5)
        }
        job_defaults = {
            'coalease': True,
            'max_instances': 10,
            'misfire_grace_time':300,
        }

        if type:
            self.sched = BackgroundScheduler(jobStore=jobStore, executors=executors, job_defaults=job_defaults, timezone='Asia/Shanghai')
        else:
            self.sched = BackgroundScheduler(timezone='Asia/Shanghai')

    def job_listener(self,Event):
        job = self.sched.get_job(Event.job_id)
        close_old_connections()
        if not Event.exception:
            print('任务正常运行！')
            try:
                Task.objects.filter(id=Event.job_id).update(taskResult='完成', nexttime= datetime.strptime(datetime.strftime(job.next_run_time,'%Y-%m-%d %H:%M:%S'),'%Y-%m-%d %H:%M:%S'))
            except Exception as e:
                Task.objects.filter(id=Event.job_id).update(taskResult='完成', nexttime=datetime.strptime(
                    datetime.strftime(job.next_run_time, '%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S'))
            logger.info("jobname=%s|jobtrigger=%s|jobtime=%s|retval=%s", job.name, job.trigger,
                        Event.scheduled_run_time, Event.retval)

        else:
            print("任务出错了！！！！！")
            try :
                Task.objects.filter(id=Event.job_id).update(taskResult='失败', nexttime= datetime.strptime(datetime.strftime(job.next_run_time,'%Y-%m-%d %H:%M:%S'),'%Y-%m-%d %H:%M:%S'))
            except Exception as e:
                Task.objects.filter(id=Event.job_id).update(taskResult='失败', nexttime=datetime.strptime(
                    datetime.strftime(job.next_run_time, '%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S'))
            logger.error("jobname=%s|jobtrigger=%s|errcode=%s|exception=[%s]|traceback=[%s]|scheduled_time=%s",
                         job.name,
                         job.trigger, Event.code,
                         Event.exception, Event.traceback, Event.scheduled_run_time)

        close_old_connections()

    # 添加定时任务 0 0 1 * * ? (每天1点触发)
    def create_job(self):
        if self.taskType == 'cron':
            res = self.__get_date()
            #start_date=self.sdate, end_date=self.edate,
            if self.sdate!='' and self.edate !='':
                self.sched.add_job(func=getattr(tools,self.taskfun), trigger='cron', day=res['day'], hour=res['hour'],minute=res['minutes'],
                                   args=[self.taskid], id=self.taskid,start_date=self.sdate,end_date=self.edate,name='taskname-'+self.taskid+self.taskfun)
            elif self.sdate !='':
                self.sched.add_job(func=getattr(tools,self.taskfun), trigger='cron', day=res['day'], hour=res['hour'],
                                   minute=res['minutes'],
                                   args=[self.taskid], id=self.taskid, start_date=self.sdate,name='taskname-'+self.taskid+self.taskfun)
            elif self.edate != '':
                self.sched.add_job(func=getattr(tools,self.taskfun), trigger='cron', day=res['day'], hour=res['hour'],
                                   minute=res['minutes'],
                                   args=[self.taskid], id=self.taskid, end_date=self.edate,name='taskname-'+self.taskid+self.taskfun)
            else:
                self.sched.add_job(func=getattr(tools,self.taskfun), trigger='cron', day=res['day'], hour=res['hour'],
                                   minute=res['minutes'],
                                   args=[self.taskid], id=self.taskid,name='taskname-'+self.taskid+self.taskfun)
            self.sched.add_listener(self.job_listener, EVENT_JOB_ERROR | EVENT_JOB_MISSED | EVENT_JOB_EXECUTED)
            self.sched._logger = logger

        # elif self.taskType == 'interval':
        #     res = self.__get_date()
        #
        #     self.sched.add_job(self.taskfun, 'interval', day=res['day'], hour=res['hour'], minutes=res['minutes'], start_date=self.sdate, end_date=self.edate, args=[self.taskid],id=self.taskid)
        else:
            self.sched.add_job(func=getattr(tools,self.taskfun), trigger='date', run_date=self.sdate,args=[self.taskid],id='taskid-'+self.taskid+self.taskfun,name='taskname-'+self.taskid+self.taskfun)




    def pause_job(self,taskid):
        myjob = self.sched.get_job(taskid)
        if myjob != None:
            print(myjob.name+"pause_job")
            self.sched.pause_job(taskid)

    def resume_job(self,taskid):
        myjob = self.sched.get_job(taskid)
        if myjob!=None:
            print(myjob.name + "resume_job")
            self.sched.resume_job(taskid)

    def remove_job(self,taskid):
        myjob = self.sched.get_job(taskid)
        if myjob != None:
            print(myjob.name + " remove_job")
            self.sched.remove_job(taskid)

    def get_job(self,taskid):
        myjob = self.sched.get_job(taskid)
        return myjob


'''
表达式	字段	描述
*	    任何	在每个值都触发
*/a	    任何	每隔 a触发一次
a-b  	任何	在 a-b区间内任何一个时间触发（ a必须小于 b）
a-b/c	任何	在 a-b区间内每隔 c触发一次
xth y	day	    第 x个星期 y触发
lastx	day	    最后一个星期 x触发
last	day	    一个月中的最后一天触发
x,y,z	任何	可以把上面的表达式进行组合
'''