# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
import logging

from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Q, Case, When, F, Value, Max, CharField
from django.db.models.functions import Concat
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from jcanayls.Dao.praseQDData import qdAnayls
from jcanayls.bd_tools.washdata import peal
from jcanayls.models import teaminfo, guangshirel, peilvqujian, teamhistroy, Vsteaminfo, Teamseaon, vsmatch, odddata, \
    ConciseTeamNews, aiarticle, TeamNews
from public.parseFile import parseQdInfo
from public.redisOps import RedisOps
from public.request import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
import json
from django.utils import timezone

weeks = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']


# 接口条件查询
@login_required()
def baseManage(request, qdList=None):
    countryName = request.GET.get('countryName', '')
    liansaiName = request.GET.get('liansaiName', '')
    country = teaminfo.objects.values('country').all().order_by('country')
    countryList = list(teaminfo.objects.values('country').distinct().order_by('country'))
    if countryName == '' and liansaiName == '':
        return render(request, "app/jcanayls/basejc.html", {"countryList": list(countryList)})
    elif countryName != '' and liansaiName == '':
        liansai = teaminfo.objects.values('liansai').filter(country=countryName).order_by('liansai')
        liansaiList = list(teaminfo.objects.values('liansai').filter(country=countryName).distinct().order_by('liansai'))
        return render(request, "app/jcanayls/basejc.html",
                      {"countryList": list(countryList), "countryName": countryName, "liansaiList": liansaiList})
    else:
        liansai = teaminfo.objects.values('liansai').filter(country=countryName)
        liansaiList = list(teaminfo.objects.values('liansai').filter(country=countryName).distinct().order_by('liansai'))
        return render(request, "app/jcanayls/basejc.html",
                      {"countryList": list(countryList), "countryName": countryName, "liansaiList": liansaiList,
                       "liansaiName": liansaiName, 'qdList': qdList})


# 球队信息添加及修改
@csrf_exempt
@login_required()
def qiuduiinfo(request):
    id = request.POST.get('qdID', '')
    qiuduiName = request.POST.get('qiuduiname', '')
    country = request.POST.get('country', '')
    qdguangshi = request.POST.get('qdguangshi', '')
    liansai = request.POST.get('liansai', '')
    quanchengname = request.POST.get('quancheng', '')
    if id == '':
        if len(set([qiuduiName, country, qdguangshi, liansai])) == 4:
            with transaction.atomic():
                if not teaminfo.objects.filter(teamname=qiuduiName).exists():
                    teaminfo.objects.create(teamname=qiuduiName, liansai=liansai, teamguangshi=qdguangshi,
                                            country=country, quanchengname=quanchengname)
                    message = '添加完成'
                else:
                    message = '球队信息已存在'
        else:
            message = '参数不能为空'
    else:
        if len(set([qiuduiName, country, qdguangshi, liansai])) == 4:
            with transaction.atomic():
                if teaminfo.objects.filter(teamname=qiuduiName).exists():
                    teaminfo.objects.filter(id=id).update(teamname=qiuduiName, liansai=liansai,
                                                          teamguangshi=qdguangshi, country=country)
                    message = '修改完成'
                else:
                    message = '球队信息不存在'
        else:
            message = '修改参数不能为空'
    return HttpResponse(message)


# 广实区间关系表
@login_required()
def guangshiqujian(request):
    zhuteam = request.POST.get('zhuteam', '')
    keteam = request.POST.get('keteam', '')
    qujian = request.POST.get('qujian', '')

    if len(set([zhuteam, keteam, qujian])) == 3:
        with transaction.atomic():
            if not guangshirel.objects.filter(zhuteam=zhuteam, keteam=keteam, qujian=qujian).exists():
                guangshirel.objects.create(zhuteam=zhuteam, keteam=keteam, qujian=qujian)
                message = '添加完成'
    else:
        message = '修改参数不能为空'
    return HttpResponse(message)


# 区间赔率表
def qujianpeilv(request):
    qujian = request.POST.get('qujan', '')
    rangqiu = request.POST.get('rangqiu', '')
    peilv = request.POST.get('peilv', '')
    shuiwei = request.POST.get('shuiwei', '')

    if len(set([qujian, rangqiu, peilv, shuiwei])) == 4:
        with transaction.atomic():
            if not peilvqujian.objects.filter(qujian=qujian, rangqiu=rangqiu, peilv=peilv, shuiwei=shuiwei).exists():
                peilvqujian.objects.create(qujian=qujian, rangqiu=rangqiu, peilv=peilv, shuiwei=shuiwei)
                message = '添加完成'
            else:
                message = '参数已添加'
    else:
        message = '修改参数不能为空'
    return HttpResponse(message)


# 球队信息表上传
@login_required()
@csrf_exempt
def uploadFile(request):
    if request.method == 'POST':
        file_obj = request.FILES.get('file')
        if file_obj == None:
            return HttpResponse('文件不能为空')
        fp = os.path.join(settings.BASE_DIR, 'static', 'datafile', 'jcanayls')
        if not os.path.exists(fp):
            os.mkdir(fp)
        fn = os.path.join(fp, file_obj.name)
        if os.path.exists(fn):
            os.remove(fn)
        f = open(fn, 'wb+')
        for chunk in file_obj.chunks():
            f.write(chunk)
        f.close()
        ext = os.path.splitext(fn)[1]
        if ext in ['.xlsx', '.xls']:
            qiuduiList = parseQdInfo(fn)
        else:
            return HttpResponse('文件上传类型错误')
        res = saveBase(qiuduiList)
    return HttpResponse(res)


# 通过上传的文件保存数据-接口
def saveBase(scentList):
    qiuduiList = []
    try:
        if teaminfo.objects.all().count() == 0:
            for scent in scentList:
                qiuduiList.append(
                    teaminfo(teamname=scent[0], country=scent[1], liansai=scent[2], teamguangshi=scent[3]))
            teaminfo.objects.bulk_create(qiuduiList)
        else:
            for scent in scentList:
                with transaction.atomic():
                    if teaminfo.objects.filter(teamname=scent[0]).exists():
                        teaminfo.objects.filter(teamname=scent[0]).update(teamguangshi=scent[2])
                    else:
                        teaminfo.objects.create(teamname=scent[0], country=scent[1], liansai=scent[2],
                                                teamguangshi=scent[3], quanchengname=scent[4])
    except Exception as e:
        return '失败'
    return '成功'


#
# @login_required()
# def vsSaiGuo(request):
#     pvstime = request.GET.get('vstime')
#     vsList, dataList = [], []
#     vstime = saiguodata.objects.extra(select={'vstime': 'left(vstime,10)'}).values('vstime').distinct()
#     vsList.extend(vstime)
#     vsList = sorted(vsList, key=lambda vs: vs['vstime'], reverse=True)
#     if pvstime != '0':
#         curtime = datetime.datetime.now()
#         vsdata = saiguodata.objects.filter(vstime__contains=pvstime)
#         for data in vsdata:
#             tvs = datetime.datetime.strptime(data.vstime, '%Y-%m-%d %H:%M')
#             if curtime.day == tvs.day:
#                 if tvs.hour < curtime.hour - 2:
#                     dataList.append(
#                         {'matchId': data.matchId, 'leagueName': data.liansai, 'homeName': data.zhudui,
#                          'guestName': data.kedui, 'vstime': data.vstime})
#             elif curtime.day > tvs.day:
#                 dataList.append(
#                     {'matchId': data.matchId, 'leagueName': data.liansai, 'homeName': data.zhudui,
#                      'guestName': data.kedui, 'vstime': data.vstime})
#     return render(request, 'app/jcanayls/vssaiguo-del.html',
#                   {'vscreattime': pvstime, 'dataList': dataList, 'vslist': vsList})
#
#
# 创建logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# 创建控制台处理器
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# 创建格式化器并将其添加到处理器
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)

# 将处理器添加到logger
logger.addHandler(ch)

team_mapping = {
    '曼彻斯特城': '曼城',
    '纽卡斯尔联': '纽卡斯尔联',
    '阿森纳': '阿森纳'
}
from datetime import datetime


def get_team_news(hteamname, gteamname):
    # 使用匹配字典进行查找
    hteam_match = team_mapping.get(hteamname, hteamname)
    gteam_match = team_mapping.get(gteamname, gteamname)

    logger.debug(f'主队: {hteamname}')
    logger.debug(f'客队: {gteamname}')

    # 查找concise_teamnews中的匹配项
    hteam_news = ConciseTeamNews.objects.filter(news_time__gte=datetime(2024, 7, 21).strftime('%Y-%m-%d'),
                                                team_name=hteam_match).values('title', 'news_time', 'content')
    gteam_news = ConciseTeamNews.objects.filter(news_time__gte=datetime(2024, 7, 21).strftime('%Y-%m-%d'),
                                                team_name=gteam_match).values('title', 'news_time', 'content')

    logger.debug(f'主队数据: {list(hteam_news)}')
    logger.debug(f'客队数据: {list(gteam_news)}')

    return list(hteam_news), list(gteam_news)


@login_required()
def vsData(request):
    dataList = vsmatch.objects.filter(
        matchtime__gte=datetime.strptime(datetime.today().strftime('%Y-%m-%d') + ' ' + '11:00:00',
                                         '%Y-%m-%d %H:%M:%S')).order_by("-matchtime")

    # 获取hteamname和gteamname字段并匹配concise_teamnews表中的team_name
    for match in dataList:
        hteamname = match.hteamname
        gteamname = match.gteamname

        hteam_news, gteam_news = get_team_news(hteamname, gteamname)

        logger.debug(f'hteam_news: {hteam_news}')
        logger.debug(f'gteam_news: {gteam_news}')

        # 将新闻内容添加到match对象
        match.hteam_news = json.dumps(hteam_news, ensure_ascii=False)
        match.gteam_news = json.dumps(gteam_news, ensure_ascii=False)

    return render(request, 'app/jcanayls/baseanayls.html', {'dataList': dataList})


@login_required()
@csrf_exempt
def baseanayls(request):
    datalist, plList = [], []
    matchbh = request.POST.get('matchbh')
    oddobj = odddata.objects.filter(matchbh=matchbh).all().order_by('-showtime')
    oddlist = [odd for odd in oddobj]
    peal()
    # 1、赔率变化情况
    # 2、跟相同球队对镇时的区间
    # 3、截止目前关键人员的平均数据6场
    # 4.

    return HttpResponse(json.dumps(datalist))


#

#
# @login_required()
# @csrf_exempt
# def filedown(request):
#     data = {'status': True, 'msg': '下载成功', 'filePath': ''}
#     filepath = '/static/datafile/jcanayls/球队信息表.xlsx'
#     data['filePath'] = filepath
#     return JsonResponse(data)
#
#
# @login_required()
# @csrf_exempt
# def lookUpResult(request):
#     datalist, plList = [], []
#     matchid = request.POST.get('matchId')
#     qici = request.POST.get('qici')
#     qda = qdAnayls()
#     vsdata = vsqiudui.objects.get(qici=qici, matchId=matchid)
#     vsInfo = qda.anaylsDuiZhen(vsdata.oupei_addr)
#     did = saiguodata.objects.values('id').filter(qici=qici, matchId=matchid)
#     if len(did) > 0:
#         with transaction.atomic():
#             qdGS = qda.anaylsGS(liansai=vsdata.liansai, zhudui=vsdata.zhudui, kedui=vsdata.kedui,
#                                 addr=vsdata.oupei_addr)  # liansai,zhudui,kedui,addr
#
#             tinfo = teaminfo.objects.filter(teamname=vsdata.zhudui)
#             if tinfo.exists() and qdGS[0] != '':
#                 teaminfo.objects.filter(teamname=vsdata.zhudui).update(teamguangshi=qdGS[0])
#
#             ktinfo = teaminfo.objects.filter(teamname=vsdata.kedui)
#             if ktinfo.exists() and qdGS[1] != '':
#                 teaminfo.objects.filter(teamname=vsdata.kedui).update(teamguangshi=qdGS[1])
#             zhuduiguangshi = teaminfo.objects.values('teamguangshi').filter(teamname=vsdata.zhudui)
#             keduiguangshi = teaminfo.objects.values('teamguangshi').filter(teamname=vsdata.kedui)
#             zguangshi = zhuduiguangshi[0]['teamguangshi']
#             kguangshi = keduiguangshi[0]['teamguangshi']
#             vsqujian = guangshirel.objects.values('qujian').filter(zhuteam='主' + zguangshi,
#                                                                    keteam='客' + kguangshi)
#             if not curvsinfo.objects.filter(addr=vsdata.oupei_addr).exists():
#                 if vsqujian.count() > 0:
#                     curvsinfo.objects.create(sid=did[0]['id'], qujian=vsqujian[0]['qujian'],
#                                              vsinfo=json.dumps(vsInfo, ensure_ascii=False), addr=vsdata.oupei_addr)
#                 else:
#                     curvsinfo.objects.create(sid=did[0]['id'], qujian='',
#                                              vsinfo=json.dumps(vsInfo, ensure_ascii=False), addr=vsdata.oupei_addr)
#             else:
#                 if vsqujian.count() > 0:
#                     curvsinfo.objects.filter(addr=vsdata.oupei_addr).update(sid=did[0]['id'],
#                                                                             qujian=vsqujian[0]['qujian'],
#                                                                             vsinfo=json.dumps(vsInfo,
#                                                                                               ensure_ascii=False))
#                 else:
#                     curvsinfo.objects.filter(addr=vsdata.oupei_addr).update(sid=did[0]['id'], qujian='',
#                                                                             vsinfo=json.dumps(vsInfo,
#                                                                                               ensure_ascii=False))
#
#     qdinfo = saiguodata.objects.get(matchId=matchid, qici=qici, bifen__contains=':')
#     vsqd = vsqiudui.objects.filter(matchId=matchid, qici=qici)
#     vsinfo = curvsinfo.objects.filter(sid=qdinfo.id)
#     vsInfo = json.loads(vsinfo[0].vsinfo)
#     saiguo = qdinfo.bifen
#     if vsqd.exists():
#         pinglun = vsqd[0].pinglun if vsinfo[0].pinglun == None else vsinfo[0].pinglun
#     else:
#         pinglun = '' if vsinfo[0].pinglun == None else vsinfo[0].pinglun
#     zhuduiguangshi = teaminfo.objects.values('teamguangshi').filter(teamname=qdinfo.zhudui)
#     keduiguangshi = teaminfo.objects.values('teamguangshi').filter(teamname=qdinfo.kedui)
#     zguangshi = zhuduiguangshi[0]['teamguangshi']
#     kguangshi = keduiguangshi[0]['teamguangshi']
#     vsqujian = guangshirel.objects.values('qujian').filter(zhuteam='主' + zguangshi,
#                                                            keteam='客' + kguangshi)
#     if vsqujian.count() == 0:
#         datalist.append({'qujian': ''})
#         datalist.append({'peilv': ''})
#     else:
#         if '客' in vsqujian[0]['qujian']:
#             vsqj = vsqujian[0]['qujian'][1:]
#         else:
#             vsqj = vsqujian[0]['qujian']
#         if '-' in vsqj:
#             plList = vsqj.split('-')
#             plList[0] = plList[0] + "区间"
#             peilv1 = peilvqujian.objects.values('peilv').filter(qujian__contains=plList[0], shuiwei__contains='低水')
#             peilv2 = peilvqujian.objects.values('peilv').filter(qujian__contains=plList[1], shuiwei__contains='高水')
#             peilv = [pv for pv in peilv1] + [pv for pv in peilv2]
#         else:
#             plList.append(vsqj)
#             peilv = peilvqujian.objects.values('peilv').filter(qujian__in=plList)
#         datalist.append({'qujian': vsqujian[0]['qujian']})
#         if '客' in vsqujian[0]['qujian']:
#             datalist.append({'peilv': ';'.join([resvsePL(pl['peilv']) for pl in peilv])})
#         else:
#             datalist.append({'peilv': ';'.join([pl['peilv'] for pl in peilv])})
#     datalist.append({'content': vsInfo})
#     datalist.append({'weilian': qdinfo.weilian})
#     datalist.append({'libo': qdinfo.libo})
#     datalist.append({'resutl': saiguo})
#     datalist.append({'sid': qdinfo.id})
#     datalist.append({'pinglun': pinglun})
#     return HttpResponse(json.dumps(datalist))
#
#
# @login_required()
# @csrf_exempt
# def searchsaigou(request):
#     dataList = None
#     sdata = request.GET.get('startDate', '')
#     edata = request.GET.get('endDate', '')
#     lsname = request.GET.get('lsname', '')
#     sgvalue = request.GET.get('saigou', '')
#     # vstimev = saiguodata.objects.extra(select={'vstime': 'left(vstime,10)'}).values('vstime').distinct().order_by(
#     #     'vstime').last()
#     qicilist = vsqiudui.objects.values('qici').filter(qici__isnull=False).order_by("-qici").distinct()
#     liansai = saiguodata.objects.values('liansai').all().distinct()
#     tnull = [True if v != '' else False for v in [sdata, edata, lsname, sgvalue]]
#     if tnull[0]:
#         if not tnull[1]:
#             edata = datetime.date.today().strftime('%Y-%m-%d')
#
#         dataList = saiguodata.objects.extra(select={'vstime': 'left(vstime,10)'}).values('liansai', 'vstime', 'zhudui',
#                                                                                          'kedui', 'bifen', 'weilian',
#                                                                                          'libo', 'id', 'qici',
#                                                                                          'matchId').filter(
#             vstime__range=[sdata + ' 09:00', edata + ' 09:00'], bifen__contains=':')
#     if tnull[2]:
#         if dataList == None:
#             dataList = saiguodata.objects.extra(select={'vstime': 'left(vstime,10)'}).values('liansai', 'vstime',
#                                                                                              'qici',
#                                                                                              'zhudui', 'kedui', 'bifen',
#                                                                                              'weilian', 'libo', 'id',
#                                                                                              'matchId').filter(
#                 liansai=lsname, bifen__contains=':')
#         else:
#             dataList = dataList.filter(liansai=lsname)
#     if tnull[3]:
#         if dataList == None:
#             dataList = saiguodata.objects.extra(select={'vstime': 'left(vstime,10)'}).values('liansai', 'vstime',
#                                                                                              'qici',
#                                                                                              'zhudui', 'kedui', 'bifen',
#                                                                                              'weilian', 'libo', 'id',
#                                                                                              'matchId').filter(
#                 saigou=sgvalue, bifen__contains=':')
#         else:
#             dataList = dataList.filter(saigou=sgvalue)
#
#     return render(request, "app/jcanayls/saiguo.html", {"sdata": sdata, "edata": edata, "dataList": dataList,
#                                                         'qicilist': qicilist, 'liansaiList': liansai,
#                                                         'saigouList': ['胜', '平', '负'], 'lsName': lsname,
#                                                         'saigou': sgvalue})
#
#
# @login_required()
# @csrf_exempt
# def saiguo(request):
#     dataList, saiguoList = [], []
#     dzqici = request.POST.get("uptateDate", "")
#
#     sgqici = saiguodata.objects.values('qici').filter(qici__isnull=False).order_by("-vstime").first()
#     if dzqici == sgqici and len(saiguodata.objects.filter(qici=dzqici, bifen='')) == 0:
#         pass
#     else:
#         qda = qdAnayls()
#         dataList, qici = qda.giveGameOverData(dzqici)
#         for data in dataList:
#             if not saiguodata.objects.filter(qici=qici, vstime=data[4], zhudui=data[2], kedui=data[3]).exists():
#                 saiguoList.append(
#                     saiguodata(matchId=data[0], liansai=data[1], zhudui=data[2], kedui=data[3], vstime=data[4],
#                                qici=qici, zhuduipm=data[12], keduipm=data[13],
#                                bifen=data[5], weilian=json.dumps(data[6]), libo=json.dumps(data[7]), saigou=data[8]))
#             else:
#                 val = saiguodata.objects.values().filter(qici=qici, matchId=data[0])
#                 if val.count() == 1 and val[0]['bifen'] == 'VS':
#                     if data[5] == 'VS' or data[5] == '取消':
#                         curvsinfo.objects.filter(sid=val[0]['id']).delete()
#                         saiguodata.objects.filter(qici=qici, matchId=data[0]).delete()
#                     else:
#                         saiguodata.objects.filter(qici=qici, matchId=data[0]).update(bifen=data[5],
#                                                                                      zhuduipm=data[12],
#                                                                                      keduipm=data[13], saigou=data[8])
#
#             if not vsqiudui.objects.filter(oupei_addr=data[5]).exists():
#                 vsqiudui.objects.create(matchId=data[0], liansai=data[1], zhudui=data[2], kedui=data[3],
#                                         vstime=data[4], oupei_addr=data[9], peilv_addr=data[14], qici=dzqici)
#
#         with transaction.atomic():
#             saiguodata.objects.bulk_create(saiguoList)
#     for data in dataList:
#         with transaction.atomic():
#             tinfo = teaminfo.objects.filter(teamname=data[2])
#             if not tinfo.exists():
#                 teaminfo.objects.create(teamname=data[2], liansai=data[1], teamguangshi='',
#                                         country='', quanchengname=data[10])
#             else:
#                 if tinfo[0].quanchengname == None:
#                     teaminfo.objects.filter(teamname=data[2]).update(quanchengname=data[10])
#             ktinfo = teaminfo.objects.filter(teamname=data[3])
#             if not ktinfo.exists():
#                 teaminfo.objects.create(teamname=data[3], liansai=data[1], teamguangshi='',
#                                         country='', quanchengname=data[11])
#             else:
#                 if ktinfo[0].quanchengname == None:
#                     teaminfo.objects.filter(teamname=data[3]).update(quanchengname=data[11])
#     qda.closeBrower()
#     return HttpResponse("Update Finish")
#
#
# @login_required()
# @csrf_exempt
# def savepinglun(request):
#     pinglun = request.POST.get('pinglun', '')
#     sid = int(request.POST.get('sid', 0))
#     addr = request.POST.get('addr', '')
#     if sid != 0:
#         with transaction.atomic():
#             curvsinfo.objects.filter(sid=sid).update(pinglun=pinglun)
#     if addr != '':
#         with transaction.atomic():
#             vsqiudui.objects.filter(oupei_addr=addr).update(pinglun=pinglun)
#     return HttpResponse('finish')


def resvsePL(pl):
    plList = pl.split(' ')
    plList[0], plList[2] = plList[2], plList[0]
    return ' '.join(plList)


@login_required()
def teamHistory(request):
    liansai = teaminfo.objects.values('liansai').all()
    liansaiList = [t for t in set(d['liansai'] for d in liansai)]

    return teamHistoryV(liansaiList)


def teamHistoryV(liansaiList):
    qda = qdAnayls()
    for liansai in liansaiList:
        data = qda.teamHistoryPM(liansai)
        for d in data:
            teamid = teaminfo.objects.filter(quanchengname=d['teamid'])
            if teamid.count() > 0:
                with transaction.atomic():
                    if not teamhistroy.objects.filter(teamid=teamid[0].id, saiji=d['saiji']).exists():
                        teamhistroy.objects.create(teamid=teamid[0].id, saiji=d['saiji'], paiming=d['pm'],
                                                   liansai=liansai)
    qda.closeBrower()
    return HttpResponse('finish')


@login_required()
def zhanjiMangg(request):
    dataList = None
    sdata = request.GET.get('startDate', '')
    edata = request.GET.get('endDate', '')
    lsname = request.GET.get('lsname')  # 联赛
    team = request.GET.get('team')  # 队名

    liansai = Vsteaminfo.objects.values('matchname').filter(matchname__isnull=False).distinct()

    if lsname == None:
        return render(request, "app/jcanayls/league_record.html", {'liansaiList': liansai})

    teamset = Teamseaon.objects.values('teamname').filter(liansai=lsname).distinct()
    tnull = [True if v != '' else False for v in [sdata, edata]]

    if tnull[0]:
        if not tnull[1]:
            edata = datetime.date.today().strftime('%Y-%m-%d')
        with transaction.atomic():
            dataList = Vsteaminfo.objects.extra(
                select={"wills": "substring_index(will,'-',1)",
                        "willd": "substr(replace(will,substring_index(will,'-',1),''),2)",
                        "labss": "substring_index(labs,'-',1)",
                        "labsd": "substr(replace(labs,substring_index(labs,'-',1),''),2)"}).annotate(
                hwin=(Case(When(result="胜", hteamname=team, then=Concat(F("bifen"), F("gteamname"))))),
                hflat=(Case(When(result="平", hteamname=team, then=Concat(F("bifen"), F("gteamname"))))),
                hlost=(Case(When(result="负", hteamname=team, then=Concat(F("bifen"), F("gteamname"))))),
                gwin=(Case(When(result="胜", gteamname=team, then=Concat("hteamname", "bifen")))),
                gflat=(Case(When(result="平", gteamname=team, then=Concat("hteamname", "bifen")))),
                glost=(Case(When(result="负", gteamname=team, then=Concat("hteamname", "bifen"))))
            ).values('season', 'matchname', 'hteamname', 'hwin', 'hflat', 'hlost', 'gteamname', 'gwin',
                     'gflat', 'glost', 'hteampm', 'gteampm', 'wills', 'willd', 'labss', 'labsd').filter(
                Q(hteamname=team) | Q(gteamname=team),
                matchname=lsname, matchtime__range=[sdata + ' 09:00', edata + ' 09:00'])


    else:
        with transaction.atomic():
            dataList = Vsteaminfo.objects.extra(
                select={"wills": "substring_index(will,'-',1)",
                        "willd": "substr(replace(will,substring_index(will,'-',1),''),2)",
                        "labss": "substring_index(labs,'-',1)",
                        "labsd": "substr(replace(labs,substring_index(labs,'-',1),''),2)"}).annotate(
                hwin=(Case(When(result="胜", hteamname=team, then=Concat(F("bifen"), F("gteamname"))))),
                hflat=(Case(When(result="平", hteamname=team, then=Concat(F("bifen"), F("gteamname"))))),
                hlost=(Case(When(result="负", hteamname=team, then=Concat(F("bifen"), F("gteamname"))))),
                gwin=(Case(When(result="胜", gteamname=team, then=Concat("hteamname", "bifen")))),
                gflat=(Case(When(result="平", gteamname=team, then=Concat("hteamname", "bifen")))),
                glost=(Case(When(result="负", gteamname=team, then=Concat("hteamname", "bifen"))))
            ).values('season', 'mid', 'matchname', 'hteamname', 'hwin', 'hflat', 'hlost', 'gteamname', 'gwin', 'gflat',
                     'glost', 'hteampm', 'gteampm', 'wills', 'willd', 'labss', 'labsd').filter(
                Q(hteamname=team) | Q(gteamname=team), matchname=lsname).order_by('-season', 'mid')

    return render(request, "app/jcanayls/league_record.html", {"sdata": sdata, "edata": edata, "dataList": dataList,
                                                               'liansaiList': liansai, 'lsName': lsname,
                                                               'teamlist': teamset,
                                                               'team': team})


@login_required()
def oddstatist(request):
    dataList = []
    sdata = request.GET.get('startDate', '')
    edata = request.GET.get('endDate', '')
    lsname = request.GET.get('lsname')  # 联赛
    odd = request.GET.get('odd')  # 欧赔

    liansai = Vsteaminfo.objects.values('matchname').filter(matchname__isnull=False).distinct()

    if lsname == None:
        return render(request, "app/jcanayls/odd_statist.html", {'liansaiList': liansai})

    tnull = [True if v != '' else False for v in [sdata, edata]]
    dataset = []
    if tnull[0]:
        if not tnull[1]:
            edata = datetime.date.today().strftime('%Y-%m-%d')

        with transaction.atomic():
            if odd == '0':
                dataList = Vsteaminfo.objects.extra(
                    select={"wills": "substring_index(will,'-',1)"}).values('wills', 'will').annotate(
                    hwin=Max(Case(When(result="胜",
                                       then=Concat(F('season'), Value(' '), Value('['), F('mid'), Value(']'),
                                                   Value('['),
                                                   F('hteampm'), Value("] "), F("hteamname"), Value(' '), F("bifen"),
                                                   Value(' '), F("gteamname"), Value(" ["), F('gteampm'), Value("] "),
                                                   Value('='), F('labs'))), default=Value(''),
                                  output_field=CharField())),
                    hflat=Max(Case(When(result="平",
                                        then=Concat(F('season'), Value(' '), Value('['), F('mid'), Value(']'),
                                                    Value('['),
                                                    F('hteampm'), Value("] "), F("hteamname"), Value(' '), F("bifen"),
                                                    Value(' '),
                                                    F("gteamname"), Value(" ["), F('gteampm'), Value("] "), Value('='),
                                                    F('labs'))), default=Value(''), output_field=CharField())),
                    hlost=Max(Case(
                        When(result="负",
                             then=Concat(F('season'), Value(' '), Value('['), F('mid'), Value(']'), Value('['),
                                         F('hteampm'),
                                         Value("] "), F("hteamname"), Value(' '), F("bifen"), Value(' '),
                                         F("gteamname"),
                                         Value(" ["), F('gteampm'), Value("] "), Value('='), F('labs'))),
                        default=Value(''), output_field=CharField())),
                ).filter(
                    Q(will__isnull=False) & ~Q(will='') & Q(matchtime__range=[sdata + ' 09:00', edata + ' 09:00']) & Q(
                        matchname=lsname))
            else:
                dataList = Vsteaminfo.objects.extra(
                    select={"labss": "substring_index(labs,'-',1)"}).values('labss', 'labs').annotate(
                    hwin=Max(Case(When(result="胜",
                                       then=Concat(F('season'), Value(' '), Value('['), F('mid'), Value(']'),
                                                   Value('['),
                                                   F('hteampm'), Value("] "), F("hteamname"), Value(' '), F("bifen"),
                                                   Value(' '), F("gteamname"), Value(" ["), F('gteampm'), Value("] "),
                                                   Value('='), F('will'))), default=Value(''),
                                  output_field=CharField())),
                    hflat=Max(Case(When(result="平",
                                        then=Concat(F('season'), Value(' '), Value('['), F('mid'), Value(']'),
                                                    Value('['),
                                                    F('hteampm'), Value("] "), F("hteamname"), Value(' '), F("bifen"),
                                                    Value(' '),
                                                    F("gteamname"), Value(" ["), F('gteampm'), Value("] "), Value('='),
                                                    F('will'))), default=Value(''), output_field=CharField())),
                    hlost=Max(Case(
                        When(result="负",
                             then=Concat(F('season'), Value(' '), Value('['), F('mid'), Value(']'), Value('['),
                                         F('hteampm'),
                                         Value("] "), F("hteamname"), Value(' '), F("bifen"), Value(' '),
                                         F("gteamname"),
                                         Value(" ["), F('gteampm'), Value("] "), Value('='), F('will'))),
                        default=Value(''), output_field=CharField())),
                ).filter(
                    Q(labs__isnull=False) & ~Q(labs='') & Q(matchtime__range=[sdata + ' 09:00', edata + ' 09:00']) & Q(
                        matchname=lsname))

    else:
        with transaction.atomic():
            if odd == '0':
                dataList = Vsteaminfo.objects.extra(
                    select={"wills": "substring_index(will,'-',1)"}).values('wills', 'will').annotate(
                    hwin=Max(Case(When(result="胜",
                                       then=Concat(F('season'), Value(' '), Value('['), F('mid'), Value(']'),
                                                   Value('['),
                                                   F('hteampm'), Value("] "), F("hteamname"), Value(' '), F("bifen"),
                                                   Value(' '), F("gteamname"), Value(" ["), F('gteampm'), Value("] "),
                                                   Value('='), F('labs'))), default=Value(''),
                                  output_field=CharField())),
                    hflat=Max(Case(When(result="平",
                                        then=Concat(F('season'), Value(' '), Value('['), F('mid'), Value(']'),
                                                    Value('['),
                                                    F('hteampm'), Value("] "), F("hteamname"), Value(' '), F("bifen"),
                                                    Value(' '),
                                                    F("gteamname"), Value(" ["), F('gteampm'), Value("] "), Value('='),
                                                    F('labs'))), default=Value(''), output_field=CharField())),
                    hlost=Max(Case(
                        When(result="负",
                             then=Concat(F('season'), Value(' '), Value('['), F('mid'), Value(']'), Value('['),
                                         F('hteampm'),
                                         Value("] "), F("hteamname"), Value(' '), F("bifen"), Value(' '),
                                         F("gteamname"),
                                         Value(" ["), F('gteampm'), Value("] "), Value('='), F('labs'))),
                        default=Value(''), output_field=CharField())),
                ).filter(Q(will__isnull=False) & ~Q(will='') & Q(matchname=lsname))
            else:
                dataList = Vsteaminfo.objects.extra(
                    select={"labss": "substring_index(labs,'-',1)"}).values('labss', 'labs').annotate(
                    hwin=Max(Case(When(result="胜",
                                       then=Concat(F('season'), Value(' '), Value('['), F('mid'), Value(']'),
                                                   Value('['),
                                                   F('hteampm'), Value("] "), F("hteamname"), Value(' '), F("bifen"),
                                                   Value(' '), F("gteamname"), Value(" ["), F('gteampm'), Value("] "),
                                                   Value('='), F('will'))), default=Value(''),
                                  output_field=CharField())),
                    hflat=Max(Case(When(result="平",
                                        then=Concat(F('season'), Value(' '), Value('['), F('mid'), Value(']'),
                                                    Value('['),
                                                    F('hteampm'), Value("] "), F("hteamname"), Value(' '), F("bifen"),
                                                    Value(' '),
                                                    F("gteamname"), Value(" ["), F('gteampm'), Value("] "), Value('='),
                                                    F('will'))), default=Value(''), output_field=CharField())),
                    hlost=Max(Case(
                        When(result="负",
                             then=Concat(F('season'), Value(' '), Value('['), F('mid'), Value(']'), Value('['),
                                         F('hteampm'),
                                         Value("] "), F("hteamname"), Value(' '), F("bifen"), Value(' '),
                                         F("gteamname"),
                                         Value(" ["), F('gteampm'), Value("] "), Value('='), F('will'))),
                        default=Value(''), output_field=CharField())),
                ).filter(Q(labs__isnull=False) & ~Q(labs='') & Q(matchname=lsname))
    if odd == '0':
        for data in dataList:
            if data['hwin'] != "" and data['hwin'] != 'null':
                wail = data['hwin'].split('=')
                if len(wail) == 2:
                    labs = wail[1].split('-')[1] if '-' in wail else wail[1]
                else:
                    labs = '-'
            else:
                wail = ['']
                labs = '-'

            if data['hflat'] != "" and data['hflat'] != 'null':
                fae = data['hflat'].split('=')
                if len(fae) == 2:
                    labs1 = fae[1].split('-')[1] if '-' in fae else fae[1]
                else:
                    labs1 = '-'
            else:
                fae = ['']
                labs1 = '-'
            if data['hlost'] != "" and data['hlost'] != 'null':
                lag = data['hlost'].split('=')
                if len(lag) == 2:
                    labs2 = lag[1].split('-')[1] if '-' in lag else lag[1]
                else:
                    labs2 = '-'
            else:
                lag = ['']
                labs2 = '-'
            dataset.append({'wills': data['will'], 'labs': labs, 'labs1': labs1, 'labs2': labs2, 'hwin': wail[0],
                            'hflat': fae[0], 'hlost': lag[0]})
    else:
        for data in dataList:
            if data['hwin'] != "" and data['hwin'] != 'null':
                wail = data['hwin'].split('=')
                if len(wail) == 2:
                    wills = wail[1].split('-')[1] if '-' in wail else wail[1]
                else:
                    wills = '-'
            else:
                wail = ['']
                wills = '-'

            if data['hflat'] != "" and data['hflat'] != 'null':
                fae = data['hflat'].split('=')
                if len(fae) == 2:
                    wills1 = fae[1].split('-')[1] if '-' in fae else fae[1]
                else:
                    wills1 = '-'
            else:
                fae = ['']
                wills1 = '-'
            if data['hlost'] != "" and data['hlost'] != 'null':
                lag = data['hlost'].split('=')
                if len(lag) == 2:
                    wills2 = lag[1].split('-')[1] if '-' in lag else lag[1]
                else:
                    wills2 = '-'
            else:
                lag = ['']
                wills2 = '-'

            dataset.append({'labss': data['labs'], 'wills': wills, 'wills1': wills1, 'wills2': wills2, 'hwin': wail[0],
                            'hflat': fae[0], 'hlost': lag[0]})

    return render(request, "app/jcanayls/odd_statist.html", {"sdata": sdata, "edata": edata, "dataList": dataset,
                                                             'liansaiList': liansai, 'lsName': lsname, 'odd': odd})


@login_required()
def odd_prase(request):
    teamvsname = request.GET.get('teamvsname', '')

    return HttpResponse(json.dumps({}))


@login_required()
def getteamlist(request):
    lsname = request.POST.get("lsname")
    teamset = Teamseaon.objects.values('teamname').filter(liansai=lsname).distinct()
    teamlist = [t['teamname'] for t in teamset]
    return HttpResponse(json.dumps(teamlist))


team_dict = {
    '曼 城': '曼城'

}


# 处理查询球队后的结果
@login_required()
def searchQD(request):
    # 获取查询参数
    countryName = request.GET.get('countryName')
    liansaiName = request.GET.get('liansaiName')

    # 获取团队信息
    qdList = teaminfo.objects.filter(liansai=liansaiName)

    return render(request, 'app/jcanayls/basejc.html', {'qdList': qdList})

@login_required
def news_show(request):
    teamname = request.GET.get('teamname')
    date = request.GET.get('date', '2024-07-01')  # 如果没有传入日期，默认使用 '2024-07-01'

    # 使用匹配字典进行查找
    teamname = team_dict.get(teamname, teamname)

    # 查找concise_teamnews中的匹配项
    team_news = ConciseTeamNews.objects.filter(
        news_time__gte=date,
        team_name=teamname
    ).order_by('-news_time').values('title', 'news_time', 'news_types', 'content', 'img')

    # 对 news_types 字段进行分组并去重
    news_types_list = ConciseTeamNews.objects.filter(
        news_time__gte=date,
        team_name=teamname
    ).values_list('news_types', flat=True).distinct()

    # 处理 team_news 中的 img 字段，将其拆分为单个 URL,并去重
    team_news_list = []
    for news in team_news:
        if 'img' in news and news['img']:
            news['img'] = list(dict.fromkeys(news['img'].split('|')))
            # print(news['img'])

        # 处理 content 字段
        if 'content' in news:
            news['content'] = news['content'].replace('。', '<br>')
            news['content'] = news['content'].replace('：', '：<br>')

        team_news_list.append(news)


    return JsonResponse({'team_news': team_news_list, 'news_types_list': list(news_types_list)})


from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
@login_required
def get_original_article_url(request):
    title = request.GET.get('title')

    # 查找 ConciseTeamNews 表中匹配的文章
    concise_news = get_object_or_404(ConciseTeamNews, title=title)

    # 从 TeamNews 表中获取对应的原文 URL
    original_news = get_object_or_404(TeamNews, title=concise_news.title)

    # 返回原文 URL
    return JsonResponse({'url': original_news.url})


import time

import json
import logging
import requests

# 配置日志记录
logger = logging.getLogger(__name__)

def process_news_with_api(all_content):
    api_url = 'https://api.coze.cn/v3/chat'

    api_headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer pat_4O2wQtGn6gMLysP8acUG3J0UjEBD7PZbANpl8pVavkxBeYt2Be26ObtIKSBiUceB'
    }

    # 直接合并 all_content 为一个大字符串
    content = "\n".join(all_content)
    logger.debug(f'合并后的content值是{content}')

    # 构建API请求数据
    data = {
        "bot_id": "7402916465022107685",
        "user_id": "1",
        "stream": True,
        "auto_save_history": True,
        "additional_messages": [
            {
                "role": "user",
                "content": content,
                "content_type": "text"
            }
        ]
    }
    logger.debug(f'API请求数据: {data}')

    try:
        # 调用API处理内容
        response = requests.post(api_url, headers=api_headers, json=data, stream=True)
        logger.debug(f'API响应状态码: {response.status_code}')

        if response.status_code == 200:
            processed_content = ''
            buffer = ''
            completed_event_detected = False

            for chunk in response.iter_content(chunk_size=8192):
                buffer += chunk.decode('utf-8')

                for line in buffer.split('\n'):
                    if line.startswith('data:'):
                        try:
                            data_json = json.loads(line[5:])
                            # logger.debug(f'接收到的数据: {data_json}')
                            if 'event' in data_json and data_json['event'] == 'conversation.message.completed':
                                completed_event_detected = True
                                break
                            if 'content' in data_json and '标题' in data_json['content']:
                                processed_content = data_json['content']
                        except json.JSONDecodeError as e:
                            logger.error(f'JSON解码错误: {e}')
                            continue

                if completed_event_detected:
                    break

            logger.debug(f'处理后的内容: {processed_content}')
            return processed_content
        else:
            logger.error(f'API请求失败，状态码: {response.status_code}')
            return None
    except requests.RequestException as e:
        logger.error(f'API请求异常: {e}')
        return None


@login_required()
@csrf_exempt
def article_generation(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            titles = data.get('titles', [])
            if titles:
                all_content = []
                concise_ids = []
                team_name = ''
                for title in titles:
                    logger.debug(title)
                    # 将 QuerySet 转换为列表
                    concise_content = ConciseTeamNews.objects.filter(title=title).values('id', 'original_content', 'team_name')
                    for news in concise_content:
                        concise_ids.append(news['id'])
                        team_name = news['team_name']
                        all_content.append(news['original_content'])


                processed_news = process_news_with_api("".join(all_content))
                if processed_news:
                    logger.debug(f'processed_news的值是：{processed_news}')

                    current_time = timezone.now()

                    # 存储到 aiarticle 表
                    aiarticle.objects.create(
                        team_name=team_name,
                        concise_id=", ".join(map(str, concise_ids)),
                        content=processed_news,
                        create_time=current_time
                    )

                    return JsonResponse({'status': 'success', 'message': '文章生成成功'})
                else:
                    return JsonResponse({'status': 'error', 'message': '文章生成失败'})


        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)


@login_required()
@csrf_exempt
def get_generated_article(request):
    try:
        latest_article = aiarticle.objects.latest('create_time')
        return JsonResponse({
            'status': 'success',
            'article_content': latest_article.content
        })
    except aiarticle.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'No articles found.'
        }, status=404)


