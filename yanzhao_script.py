# -*- coding:utf-8 -*-

# @Author: zhaojianlin
# @Desc: 
# @Date: 2020/5/20
# @File: yanzhao_script.py

from time import time, sleep
import sys
from config import *
import requests
import json

if __name__ == '__main__':
    count = 0
    content = "1"
    url = 'https://yz.chsi.com.cn/sytj/stu/sytjqexxcx.action'
    headers = {
        'Cookie': "JSESSIONID=7E3FFF8AADC127E631320E466E0065E2; aliyungf_tc=AQAAAGNd7VO7hwcA0D/FeAPTL0rRpet/; acw_tc=2760828b15899386685083782eb317840201f6a11b36faf2ba721b2ecefd81; XSRF-CCKTOKEN=c141008d1df41416ca77936727cc2ed2; CHSICC_CLIENTFLAGYZ=d9eb3989173e58b4af1eb594997050d9; _ga=GA1.3.21980583.1589938668; _gid=GA1.3.1774950619.1589938668; zg_did=%7B%22did%22%3A%20%221722fbac981b3-06bbb267b0c123-f313f6d-1fa400-1722fbac982909%22%7D; CHSICC_CLIENTFLAGSYTJ=5c9ba779dd6e376efa331b288ea1b2ab; CHSICC_CLIENTFLAGZSML=fdc0c72e078135f955e18f6745458ca4; CHSICC_CLIENTFLAGSSWBGG=27ad0481d38a6049907ab02290e88d30; JSESSIONID=82528627FDCC95BCB4A5EC2467DA0ED1; zg_adfb574f9c54457db21741353c3b0aa7=%7B%22sid%22%3A%201589974571754%2C%22updated%22%3A%201589974572692%2C%22info%22%3A%201589938669962%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22%22%2C%22landHref%22%3A%20%22https%3A%2F%2Faccount.chsi.com.cn%2Fpassport%2Flogin%3Fentrytype%3Dyzgr%26service%3Dhttps%253A%252F%252Fyz.chsi.com.cn%252Fsytj%252Fj_spring_cas_security_check%22%2C%22cuid%22%3A%20%22418dfa901575fca52921ae50af71e5a6%22%7D"
    }
    for i in range(2):
        if count > 0:
            para = {
                'pageSize': 20,
                'start': count * 20,
                'orderBy': '',
                'mhcx': 1,
                'ssdm2': '',
                'xxfs2': '',
                'dwmc2': '软件',
                'data_type': 'json',
                'agent_from': 'wap',
                'pageid': 'tj_qe_list'
            }
        else:
            para = {
                'pageSize': 20,
                'start': '',
                'orderBy': '',
                'mhcx': 1,
                'ssdm2': '',
                'xxfs2': '',
                'dwmc2': '软件',
                'data_type': 'json',
                'agent_from': 'wap',
                'pageid': 'tj_qe_list'
            }
        r = requests.post(url, headers=headers, timeout=30, data=para)
        count += 1
        r.raise_for_status()
        r.encoding = 'utf-8'
        print(count)
        # print (r.text)
        text = json.loads(r.text)
        content = text['data']['vo_list']['vos']
        # print(content

        type_dict = {}
        type_dict['1'] = "全日制"
        type_dict['2'] = "非全日制"

        for item in parse_one_page(content):
            with open('soft.csv', 'a', encoding='utf-8-sig') as csv:
                csv.write(
                    item['schoolID'] + ',' + item['school'] + ',' + item['academic'] + ',' + item['major'] + ',' + item[
                        'majorID'] + ',' + item['direction'] + ',' + str(item['type']) + ',' + str(
                        item['remain']) + ',' + str(item['publish']) + '\n')

    pass
def parse_one_page(content):
    for item in content:
        yield {
            'school': item['dwmc'],
            'academic': item['yxsmc'],
            'major': item['zymc'],
            'majorID': item['zydm'],
            'schoolID': item['dwdm'],
            'direction': item['yjfxmc'],
            'type': type_dict[str(item['xxfs'])],
            'remain': item['qers'],
            'publish': item['gxsj']
        }
