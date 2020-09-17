#http://bang.dangdang.com/books/bestsellers/01.00.00.00.00.00-24hours-0-0-1-1
#抓取字段：书名，作者，发布时间，出版社，图书价格

import requests
from lxml import etree
import pymysql
#1.请求一个单页的内容
def get_html(url):
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'}
    response=requests.get(url,headers=headers)
    return response.text
#2.解析网页
def parse_page(html):
    html = etree.HTML(html)  #初始化
    name = html.xpath('//div[@class="name"]/a/text()')  #书名
    print(name)
    author=html.xpath('//li/div[last()-2]')  #作者
    author_new=[]
    for i in author:
        author_new.append((i.xpath('string(.)')).split('著')[0])

    ptime=html.xpath('//li/div[last()-1]/span/text()')  #发布时间
    publish=html.xpath('//li/div[last()-1]/a/text()')  #出版社
    #有的地方没有出版社数据，所以不能用test()，因为test()获取不到空值，string()可以获取到
    publish_new=[]
    for i in publish:
        publish_new.append(i.xpath('string(.)'))
    price=html.xpath('//li/div[last()]/p[1]/span[1]/text()')  #价格
    # print(len(name),len(author_new),len(ptime),len(publish),len(price)) #测试
    for i in range(0,len(name)):
        yield name[i],author_new[i],ptime[i],publish_new[i],price[i][1:] #price切片，切掉¥符号

#3.存储数据
def write_to_mysql(data):
    conn=pymysql.connect('localhost','root','zhanghao','myschool') #创建连接
    cursor=conn.cursor() #创建游标
    sql='insert into dangdangbook values (null,%s,%s,%s,%s,%s)'
    parm=tuple(data) #强转list或者tuple二元组格式
    cursor.executemany(sql,parm) #执行插入多条数据
    conn.commit() #提交
    cursor.close()
    conn.close()
#4.函数回调，分页处理
def main(page):
    #重构url
    url='http://bang.dangdang.com/books/bestsellers/01.00.00.00.00.00-24hours-0-0-1-'+str(page)
    html=get_html(url) #请求
    data=parse_page(html) #解析
    write_to_mysql(data) #存储
for i in range(1,26):  #分页处理
    main(i)
    print('当当网图书畅销榜已抓取%d页'%i)