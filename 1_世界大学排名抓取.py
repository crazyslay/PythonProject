#http://www.qianmu.org/2019USNEWS%E4%B8%96%E7%95%8C%E5%A4%A7%E5%AD%A6%E6%8E%92%E5%90%8D
#抓取字段:排名,学校中文名称,学校英文名称,所在国家

import requests
from lxml import etree
import csv

#1.向目标url发起请求
def get_html(url):
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'}
    response=requests.get(url,headers=headers)
    return response.text

#2.解析数据，构造解析规则
def parse_page(html):
    html=etree.HTML(html)  #初始化
    tr_list=html.xpath('//tr')
    # print(len(tr_list)) #测试，是否抓到所有的大学数据
    for tr in tr_list:
        index=tr.xpath('string(td[1])') #排名
        sname=tr.xpath('string(td[2])') #中文学校名称
        yname=tr.xpath('string(td[3])') #英文学校名称
        country=tr.xpath('string(td[4])') #所在国家
        yield index,sname,yname,country  #return不能返回，用yield进行迭代，类型是元祖

#3.存储数据
def write_csv(data):
    data_new=list(data) #将数据的迭代对象转换成列表
    #utf-8_sig格式设置:用csv打开python文件不会乱码
    #newline='' 参数:解决文件写入时出现多余空行
    with open('世界大学排名.csv','w',newline='',encoding='utf-8_sig') as f:
        #构建csv写入对象,f就是一个变量
        writer = csv.writer(f)
        #writerow:写入一行, writerows:写入多行
        writer.writerows(data_new)
    return '存储完成!'

#4.函数回调
url='http://www.qianmu.org/2019USNEWS%E4%B8%96%E7%95%8C%E5%A4%A7%E5%AD%A6%E6%8E%92%E5%90%8D'
html=get_html(url) #请求
data=parse_page(html) #解析
print(write_csv(data)) #存储