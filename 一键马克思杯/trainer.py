#coding=utf-8
import requests, pymysql, pprint

def get_exam_ids(usr, exid, cookie):
    url = "http://apps.ulearning.cn/exam/getExamReport?userID=%s&examID=%s" % (usr, exid)
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
    re = requests.get(url, params=data)
    examlist = []
    re = re.json()['recordArr']
    for i in re:
        examlist.append(i['paperID'])
    return examlist

def get_exam_answer(paper, usr, cookie):
    url = "http://apps.ulearning.cn/exam/getPaperAnswer?paperID=%s&userId=%s" % (paper, usr)
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
    re = requests.get(url, params=data)
    answers = {}
    for i, j in re.json().items():
        answers[i] = j['correctAnswer']
    return answers

def get_exam_title(usr, pid, cookie):
    url = "http://apps.ulearning.cn/exam/getPaperForStudent?paperID=%s&examuserId=%s" % (pid, usr)
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
    re = requests.get(url, params=data)
    titles = {}
    part = re.json()['part']
    for i in part:
        children = i['children']
        for j in children:
            if j['type'] == 1:
                titles[j['questionid']] = [1, j['title'][:40], j['item']]
            elif j['type'] == 2:
                titles[j['questionid']] = [2, j['title'][:40], j['item']]
            elif j['type'] == 3:
                titles[j['questionid']] = [3, j['title'][:40]]
            else:
                titles[j['questionid']] = [4, j['title'][:40]]
    return titles

def db_insert(examanswer, examtitle):
    conn = pymysql.connect(host='localhost', user='pyconn', password='123456',database='carlmax', charset='utf8')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    insert_dict = {}
    for i, j in examanswer.items():
        insert_dict[i] = [examtitle[int(i)], j]
    for i, j in insert_dict.items():
        if j[0][0] == 1:
            tmp = ""
            if j[1] == 'A':
                tmp = j[0][2][0]['title'][:40]
            elif j[1] == 'B':
                tmp = j[0][2][1]['title'][:40]
            elif j[1] == 'C':
                tmp = j[0][2][2]['title'][:40]
            elif j[1] == 'D':
                tmp = j[0][2][3]['title'][:40]
            sql = "insert into answers values (%s, '%s', '%s');" % (i, j[0][1], j[1] + tmp)
        elif j[0][0] == 2:
            tmp = ""
            if 'A' in j[1]:
                tmp += "A" + j[0][2][0]['title'][:10]
            if 'B' in j[1]:
                tmp += "B" + j[0][2][1]['title'][:10]
            if 'C' in j[1]:
                tmp += "C" + j[0][2][2]['title'][:10]
            if 'D' in j[1]:
                tmp += "D" + j[0][2][3]['title'][:10]
            if 'E' in j[1]:
                tmp += "E" + j[0][2][4]['title'][:10]
            if 'F' in j[1]:
                tmp += "F" + j[0][2][5]['title'][:10]
            if 'G' in j[1]:
                tmp += "G" + j[0][2][6]['title'][:10]
            sql = "insert into answers values (%s, '%s', '%s');" % (i, j[0][1], tmp)
        else:
            sql = "insert into answers values (%s, '%s', '%s');" % (i, j[0][1], j[1])
        try:
            cursor.execute(sql)
            conn.commit()
        except:
            conn.rollback()
    conn.close()

if __name__ == '__main__':
    usrid = 7849865
    examid = 33716
    cookie = '4AD8CA2F98DC8ECF6214E6F93C54E262'
    
    examlist = get_exam_ids(usrid, examid, cookie)
    #print examlist
    examtitle = get_exam_title(usrid, examlist[0], cookie)
    #print examtitle
    
    for i in examlist:
        print "Now working: " + str(i)
        try:
            examanswer = get_exam_answer(i, usrid, cookie)
            examtitle = get_exam_title(usrid, i, cookie)
        except:
            raise Exception
        db_insert(examanswer, examtitle)
    