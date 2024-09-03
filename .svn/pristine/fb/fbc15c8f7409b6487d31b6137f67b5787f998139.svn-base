# -*- coding: utf-8 -*-
import datetime
import json
import os
import re
import shutil
import time
import zipfile

from docx import Document
from jinja2 import Environment, FileSystemLoader
from openpyxl import load_workbook

from auto_ui import settings


def parseFile(filename):
    pfn = compenent(filename)
    wb = load_workbook(filename)
    scentMap = {}
    scentWay = []
    scentInter = []
    picList = {}
    falg = False
    for sname in wb.sheetnames:
        ws = wb[sname]
        if sname == '总览':
            fscentName = ''
            for r in range(3, ws.max_row):
                if ws.cell(r, 2).value != None and str.upper(ws.cell(r, 2).value) == 'END':
                    break
                scentName = ws.cell(r, 2).value
                busName = ws.cell(r, 4).value
                if scentName != None or busName != None:
                    if fscentName != '' and (fscentName != scentName or fbusName != busName):
                        scentMap.update({json.dumps(scentWay): scentInter})
                        scentWay = []
                        scentInter = []
                    if scentName != None:
                        fscentName = scentName
                        scentway = ws.cell(r, 3).value
                    if busName != None:
                        fbusName = busName
                    scentWay.append([fscentName, scentway, fbusName, ws.cell(r, 11).value])
                    scentInter.append([ws.cell(r, 5).value, ws.cell(r, 10).value])
                else:
                    scentInter.append([ws.cell(r, 5).value, ws.cell(r, 10).value])
            scentMap.update({json.dumps(scentWay): scentInter})
        elif '结果' in sname:
            resName = sname
            falg = True
        else:
            picpath = []
            fscentName = ''
            for r in range(2, ws.max_row):
                if ws.cell(r, 1).value != None and str.upper(ws.cell(r, 1).value) == 'END':
                    break
                busname = ws.cell(r, 1).value
                if busname != None:
                    if busname != fscentName and fscentName != '':
                        picList.update({'_'.join([sname, fscentName]): picpath})
                        picpath = []
                    fscentName = busname
                picN = ws.cell(r, 2).value
                picName = picN + '.png'
                picpath.append(os.path.join(pfn, picName))
            picList.update({'_'.join([sname, fscentName]): picpath})
    if falg:
        ws = wb[resName]
        fscentName = ''
        fbusName = ''
        for r in range(3, ws.max_row):
            if ws.cell(r, 2).value != None and str.upper(ws.cell(r, 2).value) == 'END':
                break
            scentName = ws.cell(r, 2).value
            busName = ws.cell(r, 4).value
            if scentName != None or busName != None:
                if fscentName != '' and (fscentName != scentName or fbusName != busName):
                    scentMap.update({json.dumps(scentWay): scentInter})
                    scentWay = []
                    scentInter = []
                if scentName != None:
                    fscentName = scentName
                if busName != None:
                    fbusName = busName
                if '_'.join([fscentName, fbusName]) in picList:
                    pname = '|'.join(picList['_'.join([fscentName, fbusName])])
                else:
                    pname = ''
                scentWay.append(
                    [fscentName, fbusName, ws.cell(r, 8).value, ws.cell(r, 9).value, pname, ws.cell(r, 12).value])
                scentInter.append([ws.cell(r, 5).value, ws.cell(r, 6).value, ws.cell(r, 7).value])
            else:
                scentInter.append([ws.cell(r, 5).value, ws.cell(r, 6).value, ws.cell(r, 7).value])
        scentMap.update({json.dumps(scentWay): scentInter})

    return scentMap


'''
Description： 读取excel中的图片，打印图片路径
  先将excel转换成zip包，解压zip包，包下面有文件夹存放了图片，读取这个图片
'''


# 判断是否是文件和判断文件是否存在
def isfile_exist(file_path):
    if not os.path.isfile(file_path):
        print("It's not a conf or no such conf exist ! %s" % file_path)
        return False
    else:
        return True


# 修改指定目录下的文件类型名，将excel后缀名修改为.zip
def change_file_name(file_path, new_type='.zip'):
    if not isfile_exist(file_path):
        return ''
    extend = os.path.splitext(file_path)[1]  # 获取文件拓展名
    if extend != '.xlsx' and extend != '.xls':
        print("It's not a excel conf! %s" % file_path)
        return False
    file_name = os.path.basename(file_path)  # 获取文件名
    new_name = str(file_name.split('.')[0]) + new_type  # 新的文件名，命名为：xxx.zip
    dir_path = os.path.dirname(file_path)  # 获取文件所在目录
    new_path = os.path.join(dir_path, new_name)  # 新的文件路径
    if os.path.exists(new_path):
        os.remove(new_path)
    shutil.copyfile(file_path, new_path)  # 保存新文件，旧文件会替换掉
    return new_path  # 返回新的文件路径，压缩包


# 解压文件
def unzip_file(zipfile_path):
    if not isfile_exist(zipfile_path):
        return False
    if os.path.splitext(zipfile_path)[1] != '.zip':
        print("It's not a zip conf! %s" % zipfile_path)
        return False
    file_zip = zipfile.ZipFile(zipfile_path, 'r')
    file_name = os.path.basename(zipfile_path)  # 获取文件名
    zipdir = os.path.join(os.path.dirname(zipfile_path), str(file_name.split('.')[0]))  # 获取文件所在目录
    for files in file_zip.namelist():
        file_zip.extract(files, os.path.join(zipfile_path, zipdir))  # 解压到指定文件目录
    file_zip.close()

    return True


# 读取解压后的文件夹，打印图片路径
def read_img(zipfile_path):
    if not isfile_exist(zipfile_path):
        return False
    dir_path = os.path.dirname(zipfile_path)  # 获取文件所在目录
    file_name = os.path.basename(zipfile_path)  # 获取文件名
    pic_dir = 'xl' + os.sep + 'media'  # excel变成压缩包后，再解压，图片在media目录
    pic_path = os.path.join(dir_path, str(file_name.split('.')[0]), pic_dir)
    if not os.path.exists(pic_path):
        zipdir = os.path.join(os.path.dirname(zipfile_path), str(file_name.split('.')[0]))
        os.remove(zipfile_path)
        shutil.rmtree(zipdir)
        return False
    file_list = os.listdir(pic_path)
    timcur = getTimeStamp()
    fn = os.path.join(settings.BASE_DIR, 'static', 'images', 'load', timcur)
    os.mkdir(fn)
    for file in file_list:
        filepath = os.path.join(pic_path, file)
        filenew = os.path.join(fn, file)
        os.rename(filepath, filenew)
    zipdir = os.path.join(os.path.dirname(zipfile_path), str(file_name.split('.')[0]))
    os.remove(zipfile_path)
    shutil.rmtree(zipdir)
    return os.path.join('static', 'images', 'load', timcur)


# 组合各个函数
def compenent(excel_file_path):
    zip_file_path = change_file_name(excel_file_path)
    if zip_file_path != '':
        if unzip_file(zip_file_path):
            return read_img(zip_file_path)


def getTimeStamp():
    curDate = datetime.datetime.now()
    dateStamp = time.mktime(curDate.timetuple())
    dateStamp = str(int(dateStamp)) + str(curDate.microsecond)[:3]
    return dateStamp


# 读取接口文件
def parseInterfaceFile(filename):
    interList = []
    wb = load_workbook(filename)
    ws = wb.active
    for r in range(3, ws.max_row + 1):
        if len(list(filter(lambda x: x.value != None, list(ws.rows)[r - 1]))) == 7:
            addr = ws.cell(r, 4).value
            ip_port = addr.split(":")
            ip_port_zs = addr.split(":")
            interMap = {"interName": ws.cell(r, 2).value, "interProtocol": ws.cell(r, 3).value, "ipAddr": ip_port[0],
                        "port": ip_port[1], "ipAddr_zs": ip_port_zs[0], "port_zs": ip_port_zs[1],
                        "reqWay": ws.cell(r, 5).value, "path": ws.cell(r, 6).value, "headStr": ws.cell(r, 7).value,
                        "bodyStr": ws.cell(r, 8).value, "projectName": ws.title}
            interList.append(interMap)
    return interList


#读取球队信息表
def parseQdInfo(fn):
    qiuduiList = []
    wb = load_workbook(fn)
    ws = wb.active
    for r in range(2,ws.max_row + 1):
        if len(list(filter(lambda x: x.value != None, list(ws.rows)[r - 1]))) == 3:
            qiuduiList.append([ws.cell(r,1).value,ws.cell(r,2).value,ws.cell(r,3).value])
    return qiuduiList

# 写接口参数到文件
def writeInterFaceData(data, filepath):
    wb = load_workbook(filepath)
    ws = wb.active
    for i, dt in enumerate(data):
        ws.cell(i + 2, 1, dt[0])
        ws.cell(i + 2, 2, dt[1])
        ws.cell(i + 2, 3, dt[2])
        ws.cell(i + 2, 4, dt[3])
        ws.cell(i + 2, 5, dt[4])
    wb.save(filepath)


def writeInterFaceMockData(data, filepath):
    wb = load_workbook(filepath)
    ws = wb.active
    for i, dt in enumerate(data):
        ws.cell(i + 2, 1, dt[0])
        ws.cell(i + 2, 2, dt[1])
        ws.cell(i + 2, 3, dt[2])
        ws.cell(i + 2, 4, dt[3])
    wb.save(filepath)


# 读取接口数据
def parseInterfaceData(filename):
    interList = []
    wb = load_workbook(filename)
    ws = wb.active()
    for rn in range(2, ws.max_row + 1):
        cols = ws.max_column
        interMap = []
        rowds = list(ws.rows)[rn - 1]
        if len(list(filter(lambda x: x.value != None, rowds))) > 4:
            proc = rowds[1].value
            for c in range(0, cols):
                if rowds[c].value != None:
                    interMap.append(rowds[c].value)
            interList.append(interMap)
    return interList


# 读取UI文件
def parseUIFile(filename):
    uiList = []
    wb = load_workbook(filename)
    ws = wb.active
    for r in range(3, ws.max_row + 1):
        if ws.cell(r, 2).value != None:
            interMap = {"elementName": ws.cell(r, 2).value, "findName": ws.cell(r, 3).value,
                        "findele": ws.cell(r, 4).value,
                        "eventName": ws.cell(r, 5).value, "eventele": ws.cell(r, 6).value, "projectName": ws.title}
            uiList.append(interMap)
    return uiList


# def readWord1(filename):
#     interList =[]
#     basetext = []
#     tmp = ''
#     doc = Document(filename)
#     itable = 1
#     tables = doc.tables
#     for d in doc.paragraphs:
#         vindex = 0
#         if d.text.strip() == '基本参数':
#             row_cells = tables[0].rows[1].cells
#             for cell in row_cells:
#                 basetext.append(cell.text.strip())
#         elif d.text.strip() == '请求参数':
#             pmap = {}
#             ppmap = {}
#             plist = []
#             index = ''
#             key = ''
#             for r,row in enumerate(tables[itable].rows):
#                 r_cells = row.cells
#                 if len(r_cells)>0 and r_cells[0].text != '' and r_cells[0].paragraphs[0].runs[0].font.strike == None:
#                     if r == 0 :
#                         for i, rv in enumerate(r_cells):
#                             if rv.text.strip() == '描述':
#                                 vindex = i
#                     elif r == 1:
#                         if 'busiCode' == r_cells[0].text.strip():
#                             interProtocol = r_cells[vindex].text.strip()
#                     elif r > 1:
#                         txt = r_cells[1].text.strip()
#                         if len(plist) > 0 and "[" not in txt:
#                             cell_text = r_cells[0].text.strip()
#                             if cell_text != '':
#                                 ppmap[cell_text] = "%(" + cell_text + ")s"
#                         elif "[" in txt:
#                             if index == '' :
#                                 plist.append({r_cells[0].text.strip():[ppmap]})
#                                 index = txt[1:2]
#                                 key = r_cells[0].text.strip()
#                             elif int(txt[1:2]) > int(index):
#                                 ppmap = {}
#                                 tlist = plist
#                                 while type(tlist) == list:
#                                     tl = tlist[len(tlist)-1]
#                                     for k in tl.keys():
#                                         if k == key:
#                                             tl[k][0].update({r_cells[0].text.strip():[ppmap]})
#                                             tlist = tl
#                                             break
#                                         else:
#                                             tlist = tl[k]
#                                 index = txt[1:2]
#                                 key = r_cells[0].text.strip()
#                             else:
#                                 ppmap = {}
#                                 if int(txt[1:2]) > 0 :
#                                     tlist = plist
#                                     while type(tlist) == list:
#                                         tl = tlist[len(tlist)-1]
#                                         for k in tl.keys():
#                                             if k == key:
#                                                 tl.update({r_cells[0].text.strip(): [ppmap]})
#                                                 tlist = tl
#                                                 break
#                                             else:
#                                                 tlist = tl[k]
#                                 else:
#                                     plist.append({r_cells[0].text.strip(): [ppmap]})
#                                     index = txt[1:2]
#                                 key = r_cells[0].text.strip()
#                         else:
#                             cell_text = r_cells[0].text.strip()
#                             if cell_text != '':
#                                 pmap[cell_text]="%("+cell_text+")s"
#             if len(plist)>0:
#                 for v in plist:
#                     pmap.update(v)
#             bodyStr = basetext[6].strip() + json.dumps(pmap) +  "}"
#             bodyStr = bodyStr.strip().replace('%(transactionType)s',interProtocol)
#             ip_p = basetext[0].split(':')
#             ip_pz = basetext[1].split(':')
#             interMap = {"interName": tmp, "interProtocol": interProtocol, "ipAddr": ip_p[0], "port": ip_p[1],
#                         "reqWay": basetext[2], "path": basetext[3],"ipAddr_zs": ip_pz[0], "port_zs": ip_pz[1],
#                         "headStr": basetext[4],"bodyStr": bodyStr, "projectName": basetext[5]}
#             interList.append(interMap)
#             itable += 2
#         else:
#             if 'Heading' in d.style.name:
#                 tmp = d.text
#
#     return interList


# 读取接口协议文档
def readWord(filename):
    interList = []
    basetext = []
    tmp = ''
    doc = Document(filename)
    itable = 1
    tables = doc.tables
    for d in doc.paragraphs:
        ele = d._p.getnext()
        if d.text.strip() == '基本参数':
            while (ele.tag != '' and ele.tag[-3:] != 'tbl'):
                ele = ele.getnext()
            if ele.tag != '':
                # print( '1:'+ tmp+':' +d.text.strip()+":")
                for aTable in tables:
                    if aTable._tbl == ele:
                        for j in range(len(aTable.columns)):
                            basetext.append(aTable.cell(1, j).text)
        elif d.text.strip() == '请求参数' or d.text.strip() == '请求消息':
            pmap = {}
            ppmap = {}
            plist = []
            interProtocol = '0'
            index = ''
            key = ''
            while (ele.tag != '' and ele.tag[-3:] != 'tbl'):
                ele = ele.getnext()
            if ele.tag != '':
                for aTable in tables:
                    if aTable._tbl == ele:
                        for i in range(1, len(aTable.rows)):
                            # print(aTable.cell(i, 0).text + '-' + aTable.cell(i, 3).text)
                            if 'busiCode' == aTable.cell(i, 0).text.strip():
                                interProtocol = aTable.cell(i, 3).text.strip()
                                if not interProtocol.isdigit():
                                    pl = re.findall(r'\（(.*?)\）', tmp)
                                    if len(pl) > 0:
                                        interProtocol = pl[0]
                                    else:
                                        continue
                            else:
                                txt = aTable.cell(i, 1).text.strip()
                                if len(plist) > 0 and "[" not in txt:
                                    cell_text = aTable.cell(i, 0).text.strip()
                                    if cell_text != '':
                                        ppmap[cell_text] = "%(" + cell_text + ")s"
                                elif "[" in txt:
                                    if index == '':
                                        plist.append({aTable.cell(i, 0).text.strip(): [ppmap]})
                                        index = txt[1:2]
                                        key = aTable.cell(i, 0).text.strip()
                                    elif int(txt[1:2]) > int(index):
                                        ppmap = {}
                                        tlist = plist
                                        while type(tlist) == list:
                                            tl = tlist[len(tlist) - 1]
                                            for k in tl.keys():
                                                if k == key:
                                                    tl[k][0].update({aTable.cell(i, 0).text.strip(): [ppmap]})
                                                    tlist = tl
                                                    break
                                                else:
                                                    tlist = tl[k]
                                        index = txt[1:2]
                                        key = aTable.cell(i, 0).text.strip()
                                    else:
                                        ppmap = {}
                                        if int(txt[1:2]) > 0:
                                            tlist = plist
                                            while type(tlist) == list:
                                                tl = tlist[len(tlist) - 1]
                                                for k in tl.keys():
                                                    if k == key:
                                                        tl.update({aTable.cell(i, 0).text.strip(): [ppmap]})
                                                        tlist = tl
                                                        break
                                                    else:
                                                        tlist = tl[k]
                                        else:
                                            plist.append({aTable.cell(i, 0).text.strip(): [ppmap]})
                                            index = txt[1:2]
                                        key = aTable.cell(i, 0).text.strip()
                                else:
                                    cell_text = aTable.cell(i, 0).text.strip()
                                    if cell_text != '':
                                        pmap[cell_text] = "%(" + cell_text + ")s"
            if len(plist) > 0:
                for v in plist:
                    pmap.update(v)
            bodyStr = basetext[6].strip().replace('%(body)s', json.dumps(pmap))
            bodyStr = bodyStr.strip().replace('%(transactionType)s', interProtocol)
            ip_p = basetext[0].split(':')
            ip_pz = basetext[1].split(':')
            interMap = {"interName": tmp, "interProtocol": interProtocol, "ipAddr": ip_p[0], "port": ip_p[1],
                        "reqWay": basetext[2], "path": basetext[3], "ipAddr_zs": ip_pz[0], "port_zs": ip_pz[1],
                        "headStr": basetext[4], "bodyStr": bodyStr, "projectName": basetext[5]}
            interList.append(interMap)
            itable += 2
        else:
            if 'Heading' in d.style.name:
                if 'cics' not in d.text:
                    if '消息' not in d.text and '参数' not in d.text:
                        if '缓存' not in d.text:
                            tmp = d.text
    return interList


def readWordMock(filename):
    interList = []
    basetext = []
    tmp = ''
    doc = Document(filename)
    itable = 1
    tables = doc.tables
    for d in doc.paragraphs:
        ele = d._p.getnext()
        if d.text.strip() == '基本参数':
            while (ele.tag != '' and ele.tag[-3:] != 'tbl'):
                ele = ele.getnext()
            if ele.tag != '':
                # print( '1:'+ tmp+':' +d.text.strip()+":")
                for aTable in tables:
                    if aTable._tbl == ele:
                        for j in range(len(aTable.columns)):
                            basetext.append(aTable.cell(1, j).text)
        elif d.text.strip() == '响应参数' or d.text.strip() == '响应消息':
            pmap = {}
            ppmap = {}
            plist = []
            interProtocol = '0'
            index = ''
            key = ''
            while (ele.tag != '' and ele.tag[-3:] != 'tbl'):
                ele = ele.getnext()
            if ele.tag != '':
                for aTable in tables:
                    if aTable._tbl == ele:
                        for i in range(1, len(aTable.rows)):
                            # print(str(i) + '-' + aTable.cell(i, 0).text + '-' + aTable.cell(i, 3).text)
                            if 'busiCode' == aTable.cell(i, 0).text.strip():
                                interProtocol = aTable.cell(i, 3).text.strip()
                                if not interProtocol.isdigit():
                                    pl = re.findall(r'\（(.*?)\）', tmp)
                                    if len(pl) > 0:
                                        interProtocol = pl[0]
                                    else:
                                        continue
                            else:
                                txt = aTable.cell(i, 1).text.strip()
                                # print(aTable.cell(i, 0).text.strip() + '-' + txt)
                                if len(plist) > 0 and "[" not in txt:
                                    cell_text = aTable.cell(i, 0).text.strip()
                                    if cell_text != '':
                                        ppmap[cell_text] = "%(" + cell_text + ")s"
                                elif '[' in txt:
                                    if index == '':
                                        plist.append({aTable.cell(i, 0).text.strip(): [ppmap]})
                                        index = txt[1:2]
                                        key = aTable.cell(i, 0).text.strip()
                                    elif int(txt[1:2]) > int(index):
                                        ppmap = {}
                                        tlist = plist
                                        while type(tlist) == list:
                                            tl = tlist[len(tlist) - 1]
                                            for k in tl.keys():
                                                if k == key:
                                                    tl[k][0].update({aTable.cell(i, 0).text.strip(): [ppmap]})
                                                    tlist = tl
                                                    break
                                                else:
                                                    tlist = tl[k]
                                        index = txt[1:2]
                                        key = aTable.cell(i, 0).text.strip()
                                    else:
                                        ppmap = {}
                                        if int(txt[1:2]) > 0:
                                            tlist = plist
                                            while type(tlist) == list:
                                                tl = tlist[len(tlist) - 1]
                                                for k in tl.keys():
                                                    if k == key:
                                                        tl.update({aTable.cell(i, 0).text.strip(): [ppmap]})
                                                        tlist = tl
                                                        break
                                                    else:
                                                        tlist = tl[k]
                                        else:
                                            plist.append({aTable.cell(i, 0).text.strip(): [ppmap]})
                                            index = txt[1:2]
                                        key = aTable.cell(i, 0).text.strip()
                                else:
                                    cell_text = aTable.cell(i, 0).text.strip()
                                    if cell_text != '':
                                        pmap[cell_text] = "%(" + cell_text + ")s"
            if len(plist) > 0:
                for v in plist:
                    pmap.update(v)
            bodyStr = basetext[2].strip().replace('%(body)s', json.dumps(pmap))
            bodyStr = bodyStr.strip().replace('%(transactionType)s', interProtocol)
            if interProtocol != '':
                interMap = {"interName": tmp, "interProtocol": interProtocol,
                            "headStr": basetext[0], "bodyStr": bodyStr, "projectName": basetext[1]}
                interList.append(interMap)
            itable += 2
        else:
            if 'Heading' in d.style.name:
                if 'cics' not in d.text:
                    if '消息' not in d.text and '参数' not in d.text:
                        if '缓存' not in d.text:
                            tmp = d.text
    return interList


# 生成Jmeter文件
def genJemterFile(data, sfp, fn, fp):
    env = Environment(loader=FileSystemLoader(sfp), trim_blocks=True, lstrip_blocks=True)
    template = env.get_template(fn)
    result = template.render(data)
    try:
        with open(fp, 'wb+') as f:
            f.write(result.encode('utf-8'))
    except Exception as e:
        return False
    return True


# 创建文件
def mkdir_file(fp):
    if not os.path.exists(fp):
        os.mkdir(fp)


# 复制文件
def copyFile(sfp, dfp):
    if os.path.exists(dfp):
        os.remove(dfp)
        shutil.copyfile(sfp, dfp)
    else:
        shutil.copyfile(sfp, dfp)


# 生成接口参数文档
def getDataParamFile(fn, pset):
    wb = load_workbook(fn)
    ws = wb.active
    t = 0
    for i, r in enumerate(pset):
        if i == 0:
            t = 3
        else:
            t += 1
        ws.cell(t, 1, r)
    wb.save(fn)


# 解析接口参数的数据
def parseInterfaceParamData(fn):
    paramDict = []
    wb = load_workbook(fn)
    ws = wb.active
    for row in range(2, ws.max_row + 1):
        paramDict.append([ws.cell(row, 2).value if ws.cell(row, 2).value != None else '',
                          ws.cell(row, 3).value if ws.cell(row, 3).value != None else '',
                          ws.cell(row, 4).value if ws.cell(row, 4).value != None else ''])
    return paramDict
