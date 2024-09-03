# -*- coding: utf-8 -*-
import json

from django.db.models import Q

from jcanayls.models import teaminfo, teamhistroy, guangshirel,peilvqujian


class jc_Dao:
    def __init__(self):
        self.gs = {'1': '人强', '2,3': '普强', '4': '准强', '5': '中强', '6,7,8,9': '中上', '10,11,12,13': '中游','14,15,16,17': '中下', '18,19,20,21,22,23,24,25': '下游'}
        self.hispm = [0.55,0.25,0.1,0.1]
        self.fenshu = {'人强': 9.3, '普强': 8.9, '准强': 8.5, '中强': 7.8, '中上': 7.2, '中游': 6.5,  '中下': 4.5, '下游': 0, }

    def qiuduiGS(self,liansai, teamname,paiming):
        tol = 0
        teamPmData = []
        zhuduiGS ,sqjgs = '','下游'
        teamdata = teaminfo.objects.filter(teamname__contains=teamname)
        if teamdata.exists():
            teamPmData = teamhistroy.objects.filter(teamid=teamdata[0].id,liansai=liansai)
        for key in self.gs.keys():
            if int(paiming) > 20:
                zhuduiGS = '下游'
                break
            if paiming in key.split(','):
                zhuduiGS = self.gs[key]
                break
        if len(teamPmData)>0:
            num = teamPmData.count()
        else:
            num = 0
        if num > 0:
            if num > 4:
                num = 4
            for n in range(num):
                for key in self.gs.keys():
                    if str(teamPmData[n].paiming) in key.split(','):
                        sjgs = self.gs[key]
                        tol = tol + self.fenshu[sjgs]*self.hispm[n]
                        break
            for key,value in self.fenshu.items():
                if tol < value:
                    continue
                sqjgs = key
                break
            if zhuduiGS != '':
                curgsval = self.fenshu[sqjgs] * 0.3 + self.fenshu[zhuduiGS] * 0.7
            else:
                print('dddd')
        else:
            curgsval = self.fenshu[zhuduiGS] * 0.5
        for key,val in self.fenshu.items():
            if curgsval < val:
                continue
            zhuduiGS = key
            break
        return zhuduiGS


    # [0]:主球队名
    # [1]:客球队名
    # [2]赛果
    # [3]盘口
    # [4]威廉赔率
    def rqiuduiGS(self,datalist):
        #获取球队广实
        gs = ''
        for data in datalist:
            tmp=[]
            try:
                zhuguangshi = teaminfo.objects.values('teamguangshi').get(teamname=data[0])
                keguangshi = teaminfo.objects.values('teamguangshi').get(teamname=data[1])
                qujian = guangshirel.objects.values('qujian').get(zhuteam=zhuguangshi,keteam=keguangshi)
                saiguo = data[2]
                weilian = list(data[4])
                pankou = list(data[3])
                pvlist = peilvqujian.objects.filter(qujian=qujian)
                if len(pvlist)>0:
                   if pankou == pvlist[0]['rangqiu']:
                        if saiguo == '胜':
                            tmp.append(pankou)
                        elif saiguo == '负':
                            pass

                   else:
                       pass


                # 获取最近6场相同球队对阵结果

            except Exception :
                continue


    def curduizheng(self):

        pass