# -*- coding: utf-8 -*-
from typing import Optional

from django.db import models
# from pydantic import BaseModel, BaseConfig


class Task(models.Model):
    id = models.BigAutoField(primary_key=True)
    taskName = models.CharField('定时任务名', max_length=64, default=None)
    sdate = models.CharField('定时任务开始执行时间', max_length=64, default=None)
    edate = models.CharField('定时任务结束执行时间', max_length=64, default=None)
    runDate = models.CharField('定时任务执行时间间隔', max_length=64, default=None)
    funcMothed = models.CharField('调用的方法', max_length=64, default=None)
    taskState = models.CharField('任务执行状态1:启用，2:禁用', max_length=64, default=None)
    taskResult = models.CharField('任务执行结果 1：执行中，2：完成，-1：失败，0：未开始', max_length=64, default=None)
    funcparam = models.CharField('任务参数', max_length=64, default=None)
    taskType = models.CharField('任务类型', max_length=64, default=None)
    modytime = models.DateTimeField('修改时间', auto_now=True)
    nexttime = models.DateTimeField('修改时间', default=None)

    class Meta:
        managed = True
        db_table = 'task'
