import urllib.request
import re
import json
import urllib
from bs4 import BeautifulSoup
import logging

#配置logging
logger = logging.getLogger()
logger.setLevel('INFO')
formatter = logging.Formatter("%(message)s")
fhlr = logging.FileHandler('result.json')  #结果存入的文件名称
fhlr.setFormatter(formatter)
logger.addHandler(fhlr)

# 在json文件起始处加入一个大括号
logger.info("[")


# 需要抓取的信息的key
keyname = ['Chemical','CAS-number ','Synonyms ','Sumformula of the chemical ',
           'LC50 values to crustaceans, mg/l ','LC50 values to fishes, mg/l ',
           'Uses ','State and appearance ','Molecular weight ',
           'Vapor pressure, mmHg ','Water solubility, mg/l ','Melting point, °C ',
           'pKa ']

for page in range(4,2714):

    try:
        dictrestult = {}  #抓取结果以k-v的形式存入一个临时dict中
        url_Name = 'http://wwwp.ymparisto.fi/scripts/Kemrek/Kemrek_uk.asp?Method=MAKECHEMdetailsform&txtChemId='+str(page)
        print(url_Name)   #打印url以判断抓取到哪个网页，如果断掉后可以再断掉的位置重新开始
        f = urllib.request.urlopen(url_Name)
        soup = BeautifulSoup(f,'html.parser')

        # 设置两个临时列表，分别存储key/value
        keylist = []
        valuelist = []
        # 对 tr 标签下的内容进行遍历
        for link in soup.find_all('td'):
            i = link.get_text()     #得到标签下的纯文本
            # 用正则表达式对文本进行分析，判断内容是key 还是 value,并分别存储到临时list中
            if i != '\n' and i != '' and i != '\xa0' and not re.match('^Data.*',str(i)):
                if re.match('.*:', str(i)) or i == 'Chemical' or i == 'References':
                    keylist.append(str(i).strip(':'))
                    valuelist.append([])
                else:
                    valuelist[-1].append(i.strip('\xa0'))
        # 利用 zip 函数将key value 列表中的内容两两对应，并生成dict格式
        a = dict(zip(keylist,valuelist))

        # 字典"a" 中混有一些乱码，只提取在第18行的keyname列表中的key,并存入临时字典 dictresult中，并写入文件
        for key in keyname:
            if key in a.keys():
                dictrestult[key] = a[key]
        if "Chemical" in a.keys():
            dictrestult['url'] = url_Name
        if len(dictrestult) != 0:
            result = json.dumps(dictrestult,indent=4)
            logger.info(result+',')
    except OSError:
        pass
    continue

logger.info(']')

# 最终要在生成的json文件中最后一个"}"符号后的 逗号 删除。
