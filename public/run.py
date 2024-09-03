#!/usr/bin/python
# -*- encoding:UTF-8 -*-
# from public.HTMLTestRunner import *
# import HTMLTestRunner,os,time
import datetime
import re
import sys
import time

from UITest.UI.appiumConfig import AppiumConfig
from UITest.UI.common import resultValit
from UITest.UI.local_element import operatorElement
from UITest.models import elementcase, element, ecResult, eleResult, picResult
from interface.models import *
from public import vaildate
from public.email import SendEmail
from public.request import *
from sysmanage.models import path, IPAddr, appconfig, product, operation, deviceconfig
from task.models import Task

email_data = {'host_dir': 'mail.zhcw.com', 'email_port': 25, 'username': 'liran@zhcw.com', 'passwd': 'lr_zhcw1212',
              'Headerfrom': 'qa@zhcw.com', 'Headerto': 'qa@zhcw.com', 'subject': '接口测试完成',
              'sender': 'qa@zhcw.com', 'receivers': ['qa@zhcw.com']}


class runTestCase:
    def __init__(self):
        pass

    def getTimeStamp(self):
        curDate = datetime.datetime.now()
        dateStamp = time.mktime(curDate.timetuple())
        dateStamp = str(int(dateStamp)) + str(curDate.microsecond)[:3]
        return dateStamp

    '''
    执行接口测试用例
    '''

    def runInterfaceTC(self, task_name, tasktimestamp, rpcparam=''):
        # 得到用例信息
        def getCaesInfo(tcID):
            inter = []
            ct = ''
            cases = testcase.objects.filter(tcID=tcID['tcID'])
            for case in cases:
                tmp = {}
                if ct == '':
                    ct = json.dumps({'tcID': case.tcID, 'testcaseName': case.testcaseName})
                intercase = interface.objects.filter(interID=case.interID).values('interID', 'interName',
                                                                                  'interProtocol',
                                                                                  'server', 'reqWay', 'path', 'headStr',
                                                                                  'bodyStr')
                yyaddr = IPAddr.objects.filter(id=intercase[0]['server']).values('ipAddr', 'ipAddr_zs', 'port',
                                                                                 'port_zs')
                yypath = path.objects.filter(id=intercase[0]['path']).values('pathName')
                tc_td = tc_data_rel.objects.get(tcID=case.id)
                td = tcData.objects.get(id=tc_td.dataID)
                tmp.update(intercase[0])
                tmp.update({'param': td.param, 'yresualt': td.resutl, 'validateWay': case.validateWay})
                tmp.update(yyaddr[0])
                tmp.update(yypath[0])
                inter.append(tmp)
            return {ct: inter}

        def getBody(interval, resp):
            paramdict = json.loads(interval['param'])
            bodystr = interval['bodyStr']
            if 'interName' in paramdict.keys():
                paramdict.pop('interName')
            for k, v in paramdict.items():
                key = '%(' + k + ')s'
                if key in bodystr:
                    bodystr = bodystr.replace(key, v)
            if resp != {} and '%(' in bodystr:
                bodystr = parseParam(resp, bodystr)
            return bodystr

        def parseParam(resp, bodystr):
            datakeyList = re.findall(r'%\((.*?)\)s', bodystr)
            resp = json.dumps(resp)
            datastr = resp.replace(' ', '')
            for key in datakeyList:
                keys = '%(' + key + ')s'
                if 'strBefore' in key:
                    v = re.findall(r'"' + key + '":"?(.*)\W', datastr)
                else:
                    v = re.findall(r'"' + key + '":"?(.*?)\W', datastr)
                if len(v) > 0:
                    bodystr = bodystr.replace(keys, v[0])
            return bodystr

        def runInter(kvalue, resultID, check):
            resval = {}
            cookies = ''
            tcResutl = True
            for interval in kvalue:
                if check == '1':
                    if interval['port'] == 0:
                        url = 'http://' + interval['ipAddr'] + '/' + interval['pathName']
                    else:
                        url = 'http://' + interval['ipAddr'] + ':' + str(interval['port']) + '/' + interval['pathName']
                else:
                    if interval['port_zs'] == 0:
                        url = 'http://' + interval['ipAddr_zs'] + '/' + interval['pathName']
                    else:
                        url = 'http://' + interval['ipAddr_zs'] + ':' + str(interval['port_zs']) + '/' + interval[
                            'pathName']
                body = getBody(interval, resval)
                if interval['reqWay'] == 'get':
                    parmdict = {'url': url, 'params': body.encode('utf-8'), 'headers': json.loads(interval["headStr"]),
                                'cookies': cookies}
                    response = get(**parmdict)
                else:
                    parmdict = {'url': url, 'params': body.encode('utf-8'), 'headers': json.loads(interval["headStr"]),
                                'cookies': cookies}
                    response = postbody(**parmdict)
                if 'error' not in response:
                    respRes = {}
                    cookies = response.cookies
                    js = json.loads(response.text)
                    if "message" in js.keys():
                        data = js["message"]
                    else:
                        data = js
                    for key, val in data.items():
                        if 'body' in key:
                            respRes.update(val)
                            resval.update(val)
                        else:
                            if respRes == {}:
                                respRes.update(val)
                                resval.update(val)
                            else:
                                for k, v in val.items():
                                    if k not in respRes.keys():
                                        respRes[k] = v
                                        resval[k] = v
                                    else:
                                        if respRes[k] == '':
                                            respRes[k] = v
                                            resval[k] = v
                    yresualt = json.loads(interval['yresualt'])
                    f = getattr(sys.modules[vaildate.__name__], interval['validateWay'])
                    vd = {'ydata': yresualt, 'rdata': respRes}
                    interResutl = f(**vd)
                    if interResutl:
                        state = 'pass'
                    else:
                        state = 'fail'
                        tcResutl = False
                    try:
                        tcResultInfo.objects.create(resultID=resultID['resultID'], interID=interval['interID'],
                                                    state=state, actResult=json.dumps(data, ensure_ascii=False))
                    except Exception as e:
                        print(e)
                else:
                    tcResutl = data
                    tcResultInfo.objects.create(resultID=resultID['resultID'], interID=interval['interID'],
                                                state='Error', actResult=json.dumps(data, ensure_ascii=False))
                    break
            return tcResutl

        taskConcord = Task.objects.values("taskConcord").get(taskName=task_name, taskActType='接口')
        dicCon = json.loads(taskConcord['taskConcord'])
        tcIDs = testcase.objects.distinct().values('tcID').filter(platformID=dicCon['plat'], produceID=dicCon['produc'],
                                                                  projectID=dicCon['porject'], del_state=0)
        cases = []
        for tcID in tcIDs:
            cases.append(getCaesInfo(tcID))
        version = self.getTimeStamp()
        for case in cases:
            for ckey, kvalue in case.items():
                k = json.loads(ckey)
                errornum = 0
                try:
                    tcResult.objects.create(tcID=k['tcID'], resultName=tasktimestamp, runAuthor='', state='run',
                                            version=version, env=dicCon['check'])
                    resultID = tcResult.objects.values("resultID").get(version=version, tcID=k['tcID'])
                    while True:
                        interResutl = runInter(kvalue, resultID, dicCon['check'])
                        if not isinstance(interResutl, bool) and 'Error' in interResutl and errornum < 4:
                            errornum += 1
                            continue
                        else:
                            break
                    if interResutl:
                        tcResult.objects.filter(version=version, tcID=k['tcID']).update(state='pass')
                    elif not isinstance(interResutl, bool) and 'Error' in interResutl:
                        #     发邮件
                        sendemail = SendEmail(email_data['host_dir'], email_data['email_port'], email_data['username'],
                                              email_data['passwd'])
                        sendemail.add_message(interResutl)
                        sendemail.add_header(email_data['Headerfrom'], email_data['Headerto'], email_data['subject'])
                        sendemail.send(email_data['sender'], email_data['receivers'].split(','))
                    else:
                        tcResult.objects.filter(version=version, tcID=k['tcID']).update(state='fail')
                except Exception as e:
                    print(e)
                    raise e

    '''
    执行UI测试用例
    '''

    def runUItestTC(self, task_name, tasktimestamp, rpcparam=''):
        devList = deviceconfig.objects.all()
        devOnlineList = AppiumConfig().haveAPPDevicesList()
        for ondev in devOnlineList:
            dev = [d for d in devList if ondev == d.deviceName]
            if len(dev) == 1:
                self.startUItest(task_name, tasktimestamp, dev, rpcparam)
            else:
                print("请确认设备连接正常--" + dev)

    # @threads(5)
    def startUItest(self, task_name, tasktimestamp, dev, rpcparam=''):

        def getCaseinfo(tcid):
            eleList = []
            caseList = elementcase.objects.filter(caseID=tcid['caseID']).order_by('caseID','num')
            for ele in caseList:
                methodName = []
                volityname = ''
                ele_value = element.objects.get(eleID=ele.eleID, delete=0)
                if ele_value.findid != 0:
                    methodName.append(operation.objects.get(id=ele_value.findid).operationName)
                if ele_value.eventid != 0:
                    methodName.append(operation.objects.get(id=ele_value.eventid).operationName)
                if ele.valitid != -1:
                    volityname = operation.objects.get(id=ele.valitid).operationName
                eleList.append(
                    {'eleID': ele_value.eleID, 'elementName': ele_value.elementName,
                     'findele': ele_value.findele,
                     'eventele': ele_value.eventele, 'methodName': methodName, 'volityname': volityname})
            return {json.dumps({'caseID': caseList[0].caseID, 'testcaseName': caseList[0].testcaseName}): eleList}

        def runUI(caseid, elevalue, resultCID, pName, ver):
            tcResutl = ""
            tcPic = False
            comm = resultValit()
            for ele in elevalue:
                time.sleep(1)
                bpath = os.path.join(settings.BASE_DIR, 'static', 'images', 'appui', 'base', pName)
                rpath = os.path.join(settings.BASE_DIR, 'static', 'images', 'appui', 'result', pName)
                if not os.path.exists(rpath):
                    os.mkdir(rpath)
                if not os.path.exists(bpath):
                    os.mkdir(bpath)
                rfileName = os.path.join(rpath, caseid + str(ele['eleID']) + '.png')
                bfileName = os.path.join(bpath, caseid + str(ele['eleID']) + '.png')
                try:
                    if len(ele['methodName']) == 2:
                        findobj = getattr(ope, ele['methodName'][0])
                        eventobj = getattr(ope, ele['methodName'][1])
                        obj = findobj(json.loads(ele['findele']))
                        if json.loads(ele['eventele']) != {}:
                            eventobj(obj, json.loads(ele['eventele']))
                        else:
                            eventobj(obj)
                    else:
                        eventobj = getattr(ope, ele['methodName'][0])
                        if json.loads(ele['eventele']) != {}:
                            eventobj(json.loads(ele['eventele']))
                        else:
                            eventobj()
                    ope.get_screenshot_as_file(rfileName) # 截图
                    if len([fn for fn in os.listdir(bpath) if
                            caseid + str(ele['eleID']) == fn.split('.')[0]]) == 1:
                        tcPic = comm.compare_images([bfileName, rfileName])
                    else:
                        os.rename(rfileName, bfileName)
                        rfileName = ''

                    #结果验证过程
                    if ele['volityname'] != '':
                        volityObj = getattr(comm, ele['volityname'])
                        if ele['eledata'] != '':
                            tcPic.append(volityObj(ele['eledata']))
                    if tcPic:
                        if tcResutl != 'Failure':
                            tcResutl = 'OK'
                        eleResult.objects.create(resultID=resultCID['resultID'], eleID=ele['eleID'],
                                                 state='pass', actResult='成功')
                    else:
                        tcResutl = 'Failure'
                        eleResult.objects.create(resultID=resultCID['resultID'], eleID=ele['eleID'],
                                                 state='fail', actResult='失败')
                    if rfileName != '':
                        picResult.objects.create(resultID=resultCID['resultID'], version=ver,
                                                 dstpic=bfileName[len('F:\workspace\platform_JC'):],
                                                 srcpic=rfileName[len('F:\workspace\platform_JC'):], resutl=tcPic)

                except Exception as e:
                    tcResutl = e.args[0]
                    eleResult.objects.create(resultID=resultCID['resultID'], eleID=ele['eleID'],
                                             state='false', actResult=e)
            return tcResutl

        taskConcord = Task.objects.values('taskConcord').get(taskName=task_name, taskActType='UI')
        dicCon = json.loads(taskConcord['taskConcord'])
        # appium参数配置
        producinfo = product.objects.values('producName', 'producsair').filter(id=dicCon['produc'])
        appconfdata = appconfig.objects.get(appName=producinfo[0]['producName'])

        if len(dicCon) == 3:
            tcIDs = elementcase.objects.distinct().values('caseID').filter(platformID=dicCon['plat'],
                                                                           produceID=dicCon['produc'],
                                                                           projectID=dicCon['porject'], delete=0)
        else:
            tcIDs = elementcase.objects.distinct().values('caseID').filter(platformID=dicCon['plat'],
                                                                           produceID=dicCon['produc'], delete=0)

        cases = []
        for tcid in tcIDs:
            cases.append(getCaseinfo(tcid))
        version = self.getTimeStamp()
        ope = operatorElement(appconfdata, dev[0],
                              'http://' + dev[0].appium_addr + ':' + dev[0].appium_port + '/wd/hub')
        flag, res = ope.startAPP()
        if flag:
            for case in cases:
                for ckey, kvalue in case.items():
                    k = json.loads(ckey)
                    try:
                        ecResult.objects.create(caseID=k['caseID'], resultName=tasktimestamp, runAuthor='', state='run',
                                                version=version)
                        resultID = ecResult.objects.values("resultID").get(version=version, caseID=k['caseID'])
                        uiResutl = runUI(str(k['caseID']), kvalue, resultID, producinfo[0]['producsair'], version)

                        if uiResutl == "OK":
                            ecResult.objects.filter(version=version, caseID=k['caseID']).update(state='pass')
                        else:
                            ecResult.objects.filter(version=version, caseID=k['caseID']).update(state='fail')
                    except Exception as e:
                        print(e)
            print('UI autotest finish')
        else:
            print('app start fail, ' + res)
