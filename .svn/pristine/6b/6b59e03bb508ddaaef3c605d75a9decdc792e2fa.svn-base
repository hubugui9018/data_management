# -*-coding:utf-8-*-
import numpy
import re

from public.SqlOperator import SqlOperator


class syncData:
    def __init__(self):
        self.so = SqlOperator()

    def getProducModule(self):
        dd = []
        self.so.connectZT()
        strSql = r"SELECT p.id AS pid,m.id AS mid,p.name AS produceName,m.name AS moduleName from zt_product AS p " \
                 r"LEFT JOIN zt_module AS m ON m.root = p.id AND m.parent = 0 AND m.type='case' AND m.deleted='0' " \
                 r"WHERE date_format(p.createdDate,'%Y-%m-%d') > '2019-01-01' AND m.id !='' AND p.`status` = 'normal' AND p.deleted='0';"
        data = self.so.search(strSql)
        self.so.closeConn()

        return data

    def getProducProject(self):
        dd = []
        self.so.connectZT()
        strSql = r"SELECT pp.product,pp.project,p.name AS produceName,j.name AS projectName from zt_projectproduct AS pp " \
                 r"LEFT JOIN zt_product AS p ON p.id = pp.product AND p.deleted='0' AND p.status='normal'" \
                 r"LEFT JOIN zt_project AS j ON j.id = pp.project AND j.deleted='0' " \
                 r"WHERE date_format(p.createdDate,'%Y-%m-%d') > '2019-01-01';"

        data = self.so.search(strSql)
        self.so.closeConn()
        return data

    def getBugdata(self, strSql, type):
        dlist = []
        self.so.connectZT()
        data = self.so.search(strSql)
        self.so.closeConn()
        if len(data) > 0 :
            if type == '0':
                for d in data:
                    dlist.append({'o': d[0], 'c': d[1]})
            elif type == '1':
                for d in data:
                    dlist.append({'way': d[0], 'num': d[1]})
            elif type == '2':
                for d in data:
                    dlist.append({'type': d[0], 'num': d[1]})
            elif type == '3':
                for d in data:
                    dlist.append({'status': d[0], 'num': d[1]})
            elif type == '4':
                dList = []
                dTuple = [d for d in data if d[2] == 2]
                for d in dTuple:
                    mid = d[0]
                    dList = list(d)
                    for dd in data[1:]:
                        pid = dd[1]
                        if mid == pid:
                            dList[4] = dList[4] + dd[4]
                            dList[5] = dList[5] + dd[5]
                            dList[6] = dList[6] + dd[6]
                            dList[7] = dList[7] + dd[7]
                    dlist.append({'module_name': dList[3], 'num': int(dList[4])})
            elif type == '5':
                for d in data:
                    dlist.append({'deptName': d[0], 'num': d[1]})
            elif type == '6':
                for d in data:
                    dlist.append({'version': d[0], 'num': d[1]})
            elif type == '7':
                return data
            elif type == '8':
                dList = []
                dTuple = [d for d in data if d[2] == 2]
                for d in dTuple:
                    mid = d[0]
                    dList = list(d)
                    for dd in data[1:]:
                        pid = dd[1]
                        if mid == pid:
                            dList[4] = dList[4] + dd[4]
                            dList[5] = dList[5] + dd[5]
                            dList[6] = dList[6] + dd[6]
                            dList[7] = dList[7] + dd[7]
                    dlist.append(dList)
            elif type == '9':
                for d in data:
                    dlist.append({'openBy': d[0], 'num': d[1]})
            else:
                dlist = data
        else:
            dlist = []
        return dlist

    def testCaseReport(self, product, project):

        strsql = r"SELECT m.id AS pid,m1.id AS mid,m.`name` AS pmodename,m1.name AS modeName,c.id AS caseID," \
                 r"cs.id AS csID,r.caseResult,r.stepResults from zt_module AS m LEFT JOIN zt_module AS m1 ON m1.parent = m.id " \
                 r"LEFT JOIN zt_case AS c ON m1.id=c.module LEFT JOIN zt_casestep as cs ON cs.`case` =c.id " \
                 r"LEFT JOIN zt_testresult as r ON r.`case` =c.id WHERE m.type='case' AND m.root = %(product)s AND m.parent = %(project)s;"
        strsql = strsql % dict(product=product, project=project)
        self.so.connectZT()
        data = self.so.search(strsql)
        self.so.closeConn()
        if data == tuple():
            return None
        # data = self.getLastResult(data)
        return self.testCaseRunReult(data)

    def testCaseModule(self, moduleID):
        strSql = r"SELECT c.id,s.id,title,s.`desc`,s.expect,r.stepResults,lastRunResult,realname,lastRunDate " \
                 r"FROM zt_case AS c LEFT JOIN zt_user ON lastRunner = account " \
                 r"LEFT JOIN zt_casestep s ON s.`case` = c.id AND s.type != 'group' AND s.version = c.version" \
                 r" LEFT JOIN zt_testresult r ON r.`case` = c.id AND c.lastRunDate = r.date WHERE module=%(moduleID)s AND c.deleted = '0'  ;"
        strSql = strSql % dict(moduleID=moduleID)
        self.so.connectZT()
        data = self.so.search(strSql)
        self.so.closeConn()
        resLs = self.testCaseRunReultSync(data)
        rl, rs = self.respTestCaseModlueReult(resLs)
        return rl, rs

    def respTestCaseModlueReult(self, data):
        respR = []
        tmp = []
        title, expect, fails = [], [], []
        runState = [0, 0, 0, 0, 0]
        for d in data:
            if tmp != [] and tmp[0] != d[0]:
                if title == []:
                    title.append(tmp[2])
                respR.append([tmp[0], title, expect, fails, tmp[6], tmp[7]])
                title, expect, fails = [], [], []
            tmp = d
            if tmp[5] == 'pass':
                runState[0] = runState[0] + 1
            elif tmp[5] == 'fail':
                runState[1] = runState[1] + 1
                title.append(tmp[3])
                expect.append(tmp[4])
                fails.append(tmp[9])
            elif tmp[5] == 'blocked':
                runState[2] = runState[2] + 1
            elif tmp[5] == 'invalid':
                runState[3] = runState[3] + 1
            else:
                runState[4] = runState[4] + 1
        if title == []:
            title.append(tmp[2])
            respR.append([tmp[0], title, expect, tmp[9], tmp[6], tmp[7]])
        else:
            respR.append([tmp[0], title, expect, tmp[9], tmp[6], tmp[7]])
        return respR, runState

    def testCaseRunReult(self, data):
        strsql = r"SELECT l.`key`,l.value FROM zt_lang l WHERE module = 'testcase';"
        self.so.connectZT()
        rvalue = self.so.search(strsql)
        self.so.closeConn()
        rmap = {}
        for v in rvalue:
            rmap[v[0]] = v[1]
        resLs = []
        tmp = []
        runcount = [0, 0, 0, 0, 0]
        for d in data:
            res = d[7]
            if tmp != [] and tmp[4] != d[4]:
                runcount[0] = sum(runcount[1:])
                resLs.append([tmp[2], tmp[3], runcount[0], runcount[1], runcount[2], runcount[3], runcount[4], tmp[0],tmp[1]])
                runcount = [0, 0, 0, 0, 0]
                tmp = d
            # else:
            #     if d[2] != None:
            #         tmp = d
            if res != None:
                ressp = res.split('}')
                for r in ressp:
                    if r != '':
                        stepId = int(re.findall(r"i:(\d.*);a", r)[0])
                        if 'blocked' in r:
                            stepResult = re.findall(r"s:7:\"(\w.*)\";s:4:\"real", r)[0]
                            runcount[3] = runcount[3] + 1
                        elif 'pass' in r:
                            stepResult = re.findall(r"s:4:\"(\w.*)\";s:4:\"real", r)[0]
                            runcount[1] = runcount[1] + 1
                        elif 'fail' in r:
                            stepResult = re.findall(r"s:4:\"(\w.*)\";s:4:\"real", r)[0]
                            runcount[2] = runcount[2] + 1
                        elif 'invalid' in r:
                            stepResult = re.findall(r"s:7:\"(\w.*)\";s:4:\"real", r)[0]
                            runcount[4] = runcount[4] + 1
            else:
                runcount[4] = runcount[4] + 1
        return resLs

    def getLastResult(self, data):
        sdata = sorted(data, key=lambda x: x[3], reverse=True)
        rdata = []
        tmp = []
        for d in sdata:
            if tmp == []:
                tmp = d
            else:
                if tmp[0] == d[0]:
                    continue
                else:
                    rdata.append(tmp)
                    tmp = d
        rdata.append(tmp)
        return rdata

    def testCaseRunReultSync(self, data):
        tmp = []
        resLs = []
        for d in data:
            tmp = [v for v in d]
            res = d[5]
            if res != None:
                ressp = res.split('}')
                for r in ressp:
                    if r != '':
                        stepId = int(re.findall(r"i:(\d.*);a", r)[0])
                        if 'blocked' in r:
                            stepResult = re.findall(r"s:7:\"(\w.*)\";s:4:\"real", r)[0]
                        elif 'pass' in r:
                            stepResult = re.findall(r"s:4:\"(\w.*)\";s:4:\"real", r)[0]
                        elif 'fail' in r:
                            stepResult = re.findall(r"s:4:\"(\w.*)\";s:4:\"real", r)[0]
                        elif 'invalid' in r:
                            stepResult = re.findall(r"s:7:\"(\w.*)\";s:4:\"real", r)[0]
                        desc = r.split("s:")[4]
                        desc = re.findall(r":\"(\w.*)\";", desc)
                    if stepId == d[1]:
                        tmp[5] = stepResult
                        tmp.append(''.join(desc))
                        resLs.append(tmp)
                        break
            else:
                tmp[5] = 'NR'
                tmp.append('')
                resLs.append(tmp)
        return resLs


# if __name__ == '__main__':
#     syd = syncData()
#     # syd.syncBugRecord()
#     # syd.addCaseData()
#     # syd.testCaseRunReult(1619)
#     # syd.creatTestData_Number(75)
