#url:http://quote.eastmoney.com/center/gridlist.html#hs_a_board
#动态url:http://10.push2.eastmoney.com/api/qt/clist/get?&pn=3&pz=20&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=m:0+t:6,m:0+t:13,m:0+t:80,m:1+t:2,m:1+t:23&fields=f12,f14,f18&_=1577366180966
#动态url上面的pn参数决定网页数据的页数
#抓取字段：代码，名称，昨收
import requests
import csv

#1.请求一个单页的内容
def get_html(url):
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'}
    response=requests.get(url,headers=headers)
    return response

#2.解析网页
def parse_page(response):
    dict_json=response.json() #json解析（将json字符串解析成字典类型）
    # print(dict_json)
    dict_list=dict_json['data']['diff']
    for i in dict_list:
        yield i['f12'],i['f14'],i['f18']  #将每一条股票数据的代码，名称，昨收进行迭代

#3.存储(沪深A股.csv)
def write_to_csv(data,page):
    with open('沪深A股.csv', 'a', newline='', encoding='utf-8_sig') as f:
        # 构建csv写入对象,f就是一个变量
        writer = csv.writer(f)
        # writerow:写入一行, writerows:写入多行
        if page==1:
            writer.writerow(['代码','名称','昨收'])  #写入表头,表头只写一次，仅在第一页写
        writer.writerows(data)

#4.调用
def main(page):
    #url重构，进行格式化处理，循环page
    url='http://10.push2.eastmoney.com/api/qt/clist/get?&pn=%d&pz=20&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=m:0+t:6,m:0+t:13,m:0+t:80,m:1+t:2,m:1+t:23&fields=f12,f14,f18&_=1577366180966'%page
    response=get_html(url) #请求
    data=parse_page(response) #解析
    write_to_csv(data,page) #存储
    print('已抓取%d页'%page) #打印存储进度

#5.分页
for i in range(1,195):
    main(i)