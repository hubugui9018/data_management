# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
import json

from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from auto_ui import settings
from public.job import Job
from taskmanage.models import Task
# 任务管理页首页
from taskmanage.tools import tools


@login_required()
def taskManage(request):
    taskid = request.POST.get('id')

    delf = request.POST.get('del')
    sdate = request.POST.get('sdate')
    tasklist = Task.objects.all()
    tasknamelist = tasklist.values('taskName')
    if type(taskid) == str and taskid.isdigit():
        taskid = int(taskid)
    if delf == '1':
        try:
            with transaction.atomic():
                Task.objects.get(id=taskid).delete()
                if str(taskid) in settings.JOBMAP.keys():
                    settings.JOBMAP[str(taskid)].remove_job(str(taskid))
                    settings.JOBMAP.pop(str(taskid))
                return HttpResponse('删除完成')
        except Exception as e:
            return HttpResponse('删除失败' + e)
    username = request.user.username
    return render(request, 'app/taskmanage/taskManage.html',
                  {'tasklist': tasklist, 'tasknamelist': tasknamelist, 'taskname': taskid, 'username': username})


@login_required()
def gettaskname(request):
    taskname = []
    name = dir(tools)
    for n in name:
        if n.find('_') != 0:
            taskname.append(n)
    return HttpResponse(json.dumps(taskname))


# 添加任务
@login_required()
def addTask(request):
    msgerror = '完成'
    taskid = request.POST.get('taskid', '')
    taskName = request.POST.get('taskName', '')
    taskMethod = request.POST.get('taskMethod', '')
    taskType = 'cron'
    startDate = request.POST.get("startDate", '')
    interval = request.POST.get('cron', '')
    endDate = request.POST.get("endDate", '')
    methodparam = request.POST.get('methodparam', '')
    taskstate = request.POST.get('taskstate')
    if taskName != '':
        if taskid == '':
            if '-' not in taskName:
                msgerror = '任务名必须包含： -活动|-公益|-中奖'
            elif not Task.objects.filter(taskName=taskName).exists() or not Task.objects.filter(
                    funcparam=methodparam).exists():
                with transaction.atomic():
                    try:
                        Task.objects.create(taskName=taskName, runDate=interval, funcMothed=taskMethod,
                                            taskState=taskstate,
                                            taskResult='未执行', funcparam=methodparam, taskType=taskType, edate=endDate,
                                            sdate=startDate)
                        id = Task.objects.values('id').filter(taskName=taskName)
                        job = Job()

                        job.setparam(taskMethod, str(id[0]['id']), startDate, endDate, interval, taskType)
                        job.setSchedule(False)
                        job.create_job()
                        if taskstate == '启用':
                            job.sched.start()
                            Task.objects.filter(taskName=taskName).update(taskResult='等待执行',
                                                                          modytime=datetime.datetime.today())
                            settings.JOBMAP.update({str(id[0]['id']): job})

                        else:
                            Task.objects.filter(taskName=taskName).update(taskResult='未执行',
                                                                          modytime=datetime.datetime.today())
                            settings.JOBMAP.update({str(id[0]['id']): ''})
                    except Exception as e:
                        print(e)
                        Task.objects.filter(taskName=taskName).update(taskResult='失败',
                                                                      modytime=datetime.datetime.today())
                        msgerror = "失败：" + str(e)
            else:
                msgerror = '任务名已存在或者任务执行用例条件已存在'
        else:  # 编辑
            with transaction.atomic():
                if Task.objects.filter(id=taskid).exists() or not Task.objects.filter(
                        funcparam=methodparam).exists():

                    job = settings.JOBMAP[taskid]
                    if job is not None and job != '':
                        job.remove_job(taskid)
                    if taskstate == '启用':
                        job = Job()

                        job.setparam(taskMethod, taskid, startDate, endDate, interval,
                                     taskType)
                        job.setSchedule(False)
                        job.create_job()
                        job.sched.start()
                        Task.objects.filter(id=taskid).update(taskName=taskName, runDate=interval,
                                                              funcMothed=taskMethod, taskState=taskstate,
                                                              taskResult='等待执行', funcparam=methodparam,
                                                              taskType=taskType, edate=endDate,
                                                              sdate=startDate, modytime=datetime.datetime.today())
                    else:
                        Task.objects.filter(id=taskid).update(taskName=taskName, runDate=interval,
                                                              funcMothed=taskMethod, taskState=taskstate,
                                                              taskResult='未执行', funcparam=methodparam,
                                                              taskType=taskType, edate=endDate,
                                                              sdate=startDate, modytime=datetime.datetime.today())

                    settings.JOBMAP.update({taskid: job})
    else:
        msgerror = '设置任务名不能为空！'

    return HttpResponse(msgerror)


# 回显任务数据
@login_required()
def recvTask(request):
    taskmap = {}
    taskid = request.POST.get('id')
    if type(taskid) == str and taskid != '':
        taskval = Task.objects.filter(id=taskid)
    else:
        taskval = []

    name = dir(tools)
    taskname = []
    for n in name:
        if n.find('_') != 0:
            taskname.append(n)

    if len(taskval) > 0:
        taskmap = {'id': taskval[0].id, 'taskName': taskval[0].taskName, 'funcMothed': taskval[0].funcMothed,
                   'taskType': taskval[0].taskType, 'sdate': taskval[0].sdate,
                   'endDate': taskval[0].edate, 'funcparam': taskval[0].funcparam, 'taskState': taskval[0].taskState,
                   'runDate': taskval[0].runDate, 'funcmotheds': taskname}

    return JsonResponse(taskmap)


# 启动任务
@login_required()
def startTask(request):
    startDate = (datetime.datetime.now() + datetime.timedelta(seconds=10)).strftime("%Y-%m-%d %H:%M:%S")
    taskid = request.POST.get('id')
    taskMathed = Task.objects.filter(id=taskid)
    if len(taskMathed) > 0:
        if taskMathed[0].taskState == '禁用':
            return HttpResponse('任务禁用，请先启用！！')
        else:

            job = Job()
            # if taskMathed[0].funcMothed =='cornparsezixunall':
            #     job.setparam(taskfun=tools.cornparsezixunall, taskid=taskid, sdate=startDate, taskType='date')
            # else:
            #     job.setparam(taskfun=tools.cornparsezixunall, taskid=taskid, sdate=startDate, taskType='date')

            job.setparam(taskMathed[0].funcMothed, taskid, sdate=startDate, taskType='date')
            job.setSchedule(False)
            job.create_job()
            job.sched.start()

            return HttpResponse('启动完成')
    else:
        return HttpResponse("任务不存在")

#
# # 获取时间戳
# def getTimeStamp():
#     curDate = datetime.datetime.now()
#     dateStamp = time.mktime(curDate.timetuple())
#     dateStamp = str(int(dateStamp)) + str(curDate.microsecond)[:3]
#     return dateStamp
#
#
# def getTimeList():
#     timetuple = datetime.datetime.now().timetuple()
#     y = [timetuple[0] + i for i in range(5)]
#     M = [timetuple[1] + i for i in range(12) if (timetuple[1] + i) < 13]
#     d = [i + 1 for i in range(31)]
#     h = [i for i in range(24)]
#     m = [i for i in range(60)]
#     s = [i for i in range(60)]
#     return [y, M, d, h, m, s]
