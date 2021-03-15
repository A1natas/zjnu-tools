# coding=utf-8
import requests
import csv
import pymysql
import time

def show_answers(data, nowid):
    print "-----------------"
    print "题号: " + str(nowid)
    print "题目: " + data['questiondetail'].encode('utf-8')
    print "答案: " + data['answer'].encode('utf-8')
    print "-----------------\n"

def output_databases():
    conn = pymysql.connect(host='localhost', user='pyconn',
                           password='123456', database='carlmax', charset='utf8')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    sql = "select * from answers;"
    cursor.execute(sql)
    data = cursor.fetchall()
    fp = open('./answer.csv', 'w')
    wt = csv.writer(fp)
    for i in data:
        tmp = [i['questionid'], i['questiondetail'].encode(
            'utf-8'), i['answer'].encode('utf-8')]
        wt.writerow(tmp)
    fp.close()


def auto_answer(usrid, pid, examid, cookie):
    url = "http://apps.ulearning.cn/exam/getPaperForStudent?paperID=%s&userID=%s&examID=%s" % (
        pid, usrid, examid)
    data = {
        'Host': 'apps.ulearning.cn',
        'Connection': 'close',
        'Accept': 'application/json, text/plain, */*',
        'Origin': 'https://mexam.ulearning.cn',
        'Authorization': cookie,
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; GM1910 Build/QKQ1.190716.003; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/77.0.3865.120 MQQBrowser/6.2 TBS/045409 Mobile Safari/537.36 umoocApp umoocApp -cn',
        'Sec-Fetch-Mode': 'cors',
        'X-Requested-With': 'cn.ulearning.yxy',
        'Sec-Fetch-Site': 'same-site',
        'Referer': 'https://mexam.ulearning.cn/',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7'
    }
    conn = pymysql.connect(host='localhost', user='pyconn',
                           password='123456', database='carlmax', charset='utf8')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    re = requests.get(url, params=data)
    part = re.json()['part']
    nowid = 1
    for i in part:
        children = i['children']
        for j in children:
            sql = "select * from answers where questionid = " + str(j['questionid']) + ";"
            cursor.execute(sql)
            try:
                show_answers(cursor.fetchall()[0], nowid)
            except:
                print "题号: " + str(nowid) + "没有找到答案"
            nowid += 1

if __name__ == '__main__':
    '''
    print "1. 导出数据库为 csv 文件"
    print "2. 爬取本次考试的答案"
    print "请输入选项: "
    inp = input()
    if inp == 1:
    '''
    usrid = 7849376
    paperid = 505324
    examid = 33716
    cookie = "BF460B4C205CA387429C78D6CC38A5A0"
    auto_answer(usrid, paperid, examid, cookie)
    #output_databases()