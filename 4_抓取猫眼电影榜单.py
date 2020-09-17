#抓取猫眼电影排行
import requests
from lxml import etree
import pymysql
for num in range(10):
    url='https://maoyan.com/board/4?offset={}0'.format(num)
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'}
    response=requests.get(url,headers=headers) #发送请求
    data=response.text
    #解析
    html = etree.HTML(data)  #初始化
    rank= html.xpath('//dl[@class="board-wrapper"]/dd/i/text()')
    image = html.xpath('//img[@class="board-img"]/@data-src')
    name = html.xpath('//p[@class="name"]/a/@title')
    actr=html.xpath('//p[@class="star"]/text()')
    time=html.xpath('//p[@class="releasetime"]/text()')
    score1=html.xpath('//p[@class="score"]/i[@class="integer"]/text()')
    score2=html.xpath('//p[@class="score"]/i[@class="fraction"]/text()')
    for i in range(len(name)):
        a=[[rank[i],image[i],name[i],actr[i].strip(),time[i],score1[i]+score2[i]]]
        conn=pymysql.connect('localhost','root','zhanghao','myschool')
        cursor=conn.cursor() #创建游标
        sql='insert into 猫眼电影排行榜单 values(%s,%s,%s,%s,%s,%s)'
        cursor.executemany(sql,a)
        conn.commit() #提交
        cursor.close()
        conn.close()