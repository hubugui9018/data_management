# coding=utf-8
import json
import datetime
import re
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from jcanayls.Dao.jc_data_Dao import jc_Dao

req_list = ["https://trade.500.com/bjdc/","https://live.500.com/zqdc.php?e=","https://liansai.500.com/team/$/teamfixture/"]


class qdAnayls:

    def __init__(self):

        self.chrome_options = Options()
        # 设置chrome浏览器无界面模式
        self.chrome_options.add_argument('--headless')
        self.chrome_options.add_argument('--disable-gpu')  # 谷歌文档提到需要加上这个属性来规避bug
        self.chrome_options.add_argument('--hide-scrollbars')  # 隐藏滚动条, 应对一些特殊页面
        self.chrome_options.add_argument('--start-maximized') # 浏览器最大化
        self.chrome_options.add_argument('--incognito') # 隐身模式（无痕模式）
        self.chrome_options.add_argument('blink-settings=imagesEnabled=false')
        self.chrome_options.add_argument(
            '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36')

        self.browser = webdriver.Chrome(options=self.chrome_options)

    def haveQDInfo(self,bdqici,bdvstime):
        qdInfo = []
        dd = datetime.date.today()
        days = int(dd.day)
        moth = int(dd.month)
        # 开始请求
        self.browser.get(req_list[0])
        qici = self.browser.find_element_by_css_selector('select#expect_select>option').text[:5]

        tbody = self.browser.find_elements_by_xpath("//table[@id='vs_table']/tbody")
        for body in tbody:
            if body.get_attribute('id')!= '':
                vsdate = body.get_attribute('id')[:10]
                vdate = datetime.datetime.strptime(vsdate, '%Y-%m-%d')
                if bdvstime.date() > vdate.date():
                    continue

                if vdate.month > moth or vdate.day >= days :
                    trNodes = body.find_elements_by_css_selector('tr.vs_lines')
                    for node in trNodes:
                        value = node.get_attribute('value').replace('\'','"')[1:-1].split(',')
                        if len(value) != 0:
                            changci = re.findall(r':"(.*?)"',value[0])[0]
                            liansai = re.findall(r':"(.*?)"',value[1])[0]
                            zhudui = re.findall(r':"(.*?)"',value[2])[0]
                            if len(node.find_elements_by_xpath("td")[3].find_element_by_xpath("a").get_property('href').split('/'))>4:
                                qzhudui = node.find_elements_by_xpath("td")[3].find_element_by_xpath("a").get_property('href').split('/')[4]
                            else:
                                qzhudui = ''
                            rangqiu = re.findall(r':"(.*?)"',value[5])[0]
                            kedui = re.findall(r':"(.*?)"',value[3])[0]
                            if len(node.find_elements_by_xpath("td")[5].find_element_by_xpath("a").get_property('href').split('/'))>4:
                                qkedui = node.find_elements_by_xpath("td")[5].find_element_by_xpath("a").get_property('href').split('/')[4]
                            else:
                                qkedui = ''
                            vstime = re.findall(r':"(.*?)"',value[4])[0]

                            oupei_addr = node.find_elements_by_xpath("td")[7].find_elements_by_xpath("a")[0].get_attribute('href')
                            if len(node.find_elements_by_xpath("td")[7].find_elements_by_xpath("a")) >2:
                                peilv_addr = node.find_elements_by_xpath("td")[7].find_elements_by_xpath("a")[2].get_attribute('href')
                            else:
                                peilv_addr = ''
                            qdInfo.append([changci, liansai, zhudui, kedui, vstime, oupei_addr, peilv_addr,qzhudui,qkedui,rangqiu,qici])
        return qdInfo

    def anaylsGS(self, liansai,zhudui,kedui,addr):
        dao = jc_Dao()
        self.browser.get(addr)
        paimings = self.browser.find_elements_by_css_selector('ul.odds_hd_list')
        if len(paimings) > 0:
            atag = paimings[0].find_elements_by_css_selector('a.hd_name')
            zhuduiID = atag[0].get_property('href').split('/')[4]
            if len(paimings[0].text.split(':')) > 1:
                pm = paimings[0].text.split(':')
                zpm = pm[len(pm) - 1].strip()
            else:
                zpm = ''
            # 主队比赛积分情况
            zdInfoNode = self.browser.find_elements_by_css_selector('div.team_a')
            zhuchangNode = zdInfoNode[0].find_elements_by_css_selector('tr.tr3>td')
            zhupm = zhuchangNode[9].text.strip()
            if zpm != '' and zhupm != '':
                zhuduiGS = dao.qiuduiGS(liansai,zhudui,zpm)
            else:
                zhuduiGS = ''

            # 客队总排名
            atag = paimings[1].find_elements_by_css_selector('a.hd_name')
            kduiID = atag[0].get_property('href').split('/')[4]
            if len(paimings[1].text.split(':')) > 1:
                kpm = paimings[1].text.split(':')[1].split(' ')[0].strip()
            else:
                kpm = ''
            # 客队比赛积分情况
            kdInfoNode = self.browser.find_elements_by_css_selector('div.team_b')
            kechangNode = kdInfoNode[0].find_elements_by_css_selector('tr.tr3>td')
            kkpm = kechangNode[9].text.strip()
            if kpm != '' and kkpm != '':
                keduiGS = dao.qiuduiGS(liansai,kedui,kpm)
            else:
                keduiGS = ''
        else:
            keduiGS = ''
            zhuduiGS = ''

        saigoulist = []

        # try:
        #     self.browser.get(req_list[2].replace('$',zhuduiID))
        # except Exception as e:
        #     print(str(e))
        #     print("yichang:"+req_list[2].replace('$', zhuduiID))
        #     self.browser.get(req_list[2].replace('$', zhuduiID))
        #
        # trnodes = self.browser.find_elements_by_css_selector('table.ltable>tbody>tr')
        # for trnode in trnodes:
        #     name = trnode.find_element_by_css_selector('td.td_lteam>a').text
        #     if name in zhudui:
        #         rname = trnode.find_element_by_css_selector('td.td_rteam>a').text
        #         saiguo = trnode.find_elements_by_css_selector('td')[5].text
        #         weilian = trnode.find_elements_by_css_selector('td')[6].text
        #         pankou = trnode.find_elements_by_css_selector('td')[7].text
        #         saigoulist.append([zhudui,rname,saiguo,pankou,weilian])
        # zhuduiRGS = dao.rqiuduiGS(saigoulist)
        #
        # saigoulist = []
        # try:
        #     self.browser.get(req_list[2].replace('$', kduiID))
        # except Exception as e:
        #     print(str(e))
        #     print("yichang addr:" + req_list[2].replace('$', kduiID))
        #     self.browser.get(req_list[2].replace('$', kduiID))
        #
        # trnodes = self.browser.find_elements_by_css_selector('table.ltable>tbody>tr')
        # for trnode in trnodes:
        #     name = trnode.find_element_by_css_selector('td.td_lteam>a').text
        #     if name in kedui:
        #         rname = trnode.find_element_by_css_selector('td.td_rteam>a').text
        #         saiguo = trnode.find_elements_by_css_selector('td')[5].text
        #         weilian = trnode.find_elements_by_css_selector('td')[6].text
        #         pankou = trnode.find_elements_by_css_selector('td')[7].text
        #         saigoulist.append([kedui,rname, saiguo, pankou, weilian])
        # kduiRGS = dao.rqiuduiGS(saigoulist)


        return [zhuduiGS, keduiGS]

    def anaylsDuiZhen(self, addr):
        self.browser.get(addr)
        zhuduiZJ, keduiZJ = [], []
        paimings = self.browser.find_elements_by_css_selector('ul.odds_hd_list')
        # zhuduiName = self.browser.find_elements_by_css_selector('div.team_name')[0].text
        # keduiName = self.browser.find_elements_by_css_selector('div.team_name')[1].text
        # 主队总排名
        if len(paimings[0].text.split(':')) > 1:
            zhuduiZJ.append(paimings[0].text.replace('\n', ' '))

        # 主队比赛积分情况
        zdInfoNode = self.browser.find_elements_by_css_selector('div.team_a')
        zhuchangNode = zdInfoNode[0].find_elements_by_css_selector('tr.tr3>td')
        zhuduiZJ.append("<br>主场排名：" + zhuchangNode[9].text)

        ##主队近期战绩
        zdzhanji = zdInfoNode[1].find_elements_by_css_selector('div.M_content>table>tbody>tr')
        zhuduiZJ.append("<br>近期战绩：" + json.dumps([zj.text.split(' ')[-3] for zj in zdzhanji[2:9]], ensure_ascii=False))
        tscore = zdInfoNode[0].find_elements_by_css_selector('tr>td')
        bifenStr = [zj.text.split(' ')[1] for zj in zdzhanji[2:6]]
        for bf in bifenStr:
            bf.split('\n')
        zhuduiZJ.append(
            "<br>" + tscore[1].text + "场战绩" + tscore[2].text + "胜" + tscore[3].text + "平" + tscore[4].text + "负进" +
            tscore[5].text + "球失" + tscore[6].text + "球")
        # 主队主场战绩
        zdzczhanji = zdInfoNode[2].find_elements_by_css_selector('div.M_content>table>tbody>tr')
        zhuduiZJ.append(
            "<br>近期主场战绩：" + json.dumps([zj.text.split(' ')[-3] for zj in zdzczhanji[2:9]], ensure_ascii=False))
        zhuduiZJ.append(
            "<br>" + tscore[12].text + "场战绩" + tscore[13].text + "胜" + tscore[14].text + "平" + tscore[15].text + "负进" +
            tscore[16].text + "球失" + tscore[17].text + "球")
        # 客队总排名
        if len(paimings[1].text.split(':')) > 1:
            keduiZJ.append(paimings[1].text.replace("\n", " "))

        # 客队比赛积分情况
        kdInfoNode = self.browser.find_elements_by_css_selector('div.team_b')
        kechangNode = kdInfoNode[0].find_elements_by_css_selector('tr.tr3>td')
        keduiZJ.append("<br>客场排名：" + kechangNode[9].text)

        ##客队近期战绩
        ktscore = kdInfoNode[0].find_elements_by_css_selector('tr>td')

        kdzhanji = kdInfoNode[1].find_elements_by_css_selector('div.M_content>table>tbody>tr')
        keduiZJ.append("<br>近期战绩：" + json.dumps([zj.text.split(' ')[-3] for zj in kdzhanji[2:9]], ensure_ascii=False))
        keduiZJ.append(
            "<br>" + ktscore[1].text + "场战绩" + ktscore[2].text + "胜" + ktscore[3].text + "平" + ktscore[4].text + "负进" +
            ktscore[5].text + "球失" + ktscore[6].text + "球")

        # 客队客场战绩
        zdzczhanji = kdInfoNode[2].find_elements_by_css_selector('div.M_content>table>tbody>tr')
        keduiZJ.append(
            "<br>近期客场战绩：" + json.dumps([zj.text.split(' ')[-3] for zj in zdzczhanji[2:9]], ensure_ascii=False))
        keduiZJ.append("<br>" + ktscore[23].text + "场战绩" + ktscore[24].text + "胜" + ktscore[25].text + "平" + ktscore[
            26].text + "负进" + ktscore[27].text + "球失" + ktscore[28].text + "球")

        # 两队交锋历史
        historys = self.browser.find_elements_by_css_selector('div.history>div.M_content>table>tbody>tr')[2:]
        historyResult = "历史交锋：" + json.dumps([his.text.split('\n')[4].split(' ')[1] for his in historys],
                                             ensure_ascii=False) + "<br>" + self.browser.find_element_by_css_selector(
            'div.history>div.M_title>span.his_info').text

        return [zhuduiZJ, keduiZJ, historyResult]

    def getSaiGou(self, addr):
        self.browser.get(addr)
        saiguo = self.browser.find_element_by_css_selector('div.odds_hd_center>p.odds_hd_bf>strong').text
        return saiguo

    def getPeilv(self, addr):
        spf, dyncPl = [], []
        self.browser.get(addr)
        oupeis = self.browser.find_elements_by_css_selector('div.table_cont>table>tbody>tr')
        for oupei in oupeis[:10]:
            if '威廉' in oupei.text.split('\n')[1]:
                dyncPl = [pl.text.split(' ') for pl in
                          oupei.find_elements_by_css_selector('td')[2].find_elements_by_css_selector('table>tbody>tr')]
                spf.append(dyncPl)
            if '立博' in oupei.text.split('\n')[1]:
                dyncPl = [pl.text.split(' ') for pl in
                          oupei.find_elements_by_css_selector('td')[2].find_elements_by_css_selector('table>tbody>tr')]
                spf.append(dyncPl)
                break
        return spf

    def giveGameOverData(self,bdqici):
        qdInfo = []
        # 开始请求
        qda = qdAnayls()
        self.browser.get(req_list[1] + bdqici)
        trNodes = self.browser.find_elements_by_xpath('//table[@id="table_match"]/tbody/tr')
        time.sleep(1)
        if trNodes is not None and trNodes[0].find_element_by_xpath('td[1]').text ==1:
            return qdInfo,bdqici
        for node in trNodes:
            if node.get_property('id') != '':
                td = node.find_elements_by_tag_name("td")
                node.is_displayed()
                time.sleep(1)
                if '完' not in node.text:
                    node.location_once_scrolled_into_view
                    time.sleep(1)
                    print("finish stutas : " + node.text)
                if td is not None and '完' in node.text:
                    changci = td[0].text
                    liansai = td[1].text

                    zhuduipm = td[5].find_element_by_xpath("span[@class='gray']").text
                    zhudui = td[5].find_element_by_xpath('a').text
                    qzhudui = node.find_elements_by_xpath("td[@class='p_lr01']/a")[0].get_property('href')[29:-1]
                    kedui = td[7].find_element_by_xpath('a').text
                    keduipm = td[7].find_element_by_xpath("span[@class='gray']").text
                    qkedui = node.find_elements_by_xpath("td[@class='p_lr01']/a")[1].get_property('href')[29:-1]
                    tagA = node.find_elements_by_xpath('td/div[@class="pk"]/a')
                    saiguo = ':'.join([tagA[0].text,tagA[2].text])
                    text = td[3].text
                    y = datetime.date.today().year
                    m = datetime.date.today().month
                    if int(text[:2])>m :
                        vstime = datetime.datetime.strptime('-'.join([str(y-1),td[3].text]),'%Y-%m-%d %H:%M')
                    else:
                        vstime = datetime.datetime.strptime(
                            '-'.join([str(y), td[3].text]),
                                     '%Y-%m-%d %H:%M')
                    addr =td[11].find_elements_by_xpath('a')[
                        0].get_property('href')
                    parseadd = td[11].find_elements_by_xpath('a')[2].get_property('href')
                    peilvdata = qda.getPeilv(parseadd)

                    if len(peilvdata) > 1:
                        weilian = peilvdata[0]
                        libo = peilvdata[1]
                    else:
                        weilian = []
                        libo =[]
                    if ':' in saiguo:
                        if int(saiguo[0]) > int(saiguo[2]):
                            bifen = '胜'
                        elif int(saiguo[0]) < int(saiguo[2]):
                            bifen = '负'
                        else:
                            bifen = '平'
                    else:
                        bifen = ''
                    qdInfo.append([changci, liansai, zhudui,kedui, vstime, saiguo, weilian, libo, bifen, addr,qzhudui,qkedui,zhuduipm,keduipm,parseadd])
                    print([changci, liansai, zhudui,zhuduipm, kedui, keduipm,vstime, saiguo, weilian, libo, bifen, addr,qzhudui,qkedui])

        return qdInfo,bdqici

    def teamHistoryPM(self,liansai):
        team = []
        url = 'https://liansai.500.com/zuqiu-5283/'
        self.browser.get(url)
        optionlist = self.browser.find_elements_by_css_selector('select.lpage_race_head_sel1>option')
        for option in optionlist:
            if option.text[2:] == liansai:
                val = option.get_property('value')
                self.browser.get('https://liansai.500.com/zuqiu-'+val)
                num = len(self.browser.find_elements_by_css_selector('div.ldrop_bd>div.ldrop_bd_in>ul.ldrop_list>li'))
                if num > 5:
                    num = 5
                for i in range(num):
                    li_elem = self.browser.find_elements_by_css_selector('div.ldrop_bd>div.ldrop_bd_in>ul.ldrop_list>li')[i+1]
                    a_elem = li_elem.find_element_by_tag_name('a')
                    href = a_elem.get_property('href')
                    self.browser.get(href)
                    saiji = self.browser.find_element_by_css_selector('span.ldrop_tit_txt').text
                    elemtr = self.browser.find_elements_by_css_selector('div.lbox_bd>table.lstable1>tbody>tr')
                    for index ,tr in enumerate(elemtr[1:]):
                        # teamname = ''.join(re.findall(r'[\u4e00-\u9fa5]',tr.text))
                        teamid = tr.find_element_by_tag_name('a').get_property('href').split('/')[4]
                        team.append({'saiji':saiji,'pm':index+1,'teamid':teamid})
                break
        return team

    def closeBrower(self):
        self.browser.close()
        self.browser.quit()
