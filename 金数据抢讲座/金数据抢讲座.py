#coding:utf-8
from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options
import random
import requests
from lxml import etree

timing = '2020-12-14 19:27:00'       #定时模块，修改格式按照 '2020-12-14 19:25:20' 不要多任何字符
t = time.mktime(time.strptime(timing,"%Y-%m-%d %H:%M:%S"))
while time.time() < t:
    time.sleep(1)

driver = webdriver.Chrome()      #创建一个浏览器
information = {                  #设置信息
    "name":"test",    #姓名
    "tel":"12345678978",    #电话号码
    "stuid":"123456789789",    #学号
    "qq":"123456789",      #qq
    "class":"test",      #班级
    "sex":"男"         #性别
}

driver.get('https://jinshuju.net/f/Ty1FJk')      #浏览器访问问卷
time.sleep(0.3)        #睡一会
que = driver.find_elements_by_class_name('label-item')     #找到问题
ans = driver.find_elements_by_class_name('ant-input')       #找到写内容的地方
for i in range(len(que)):
    temp = que[i].text
    print(temp)
    if  '姓名' in temp or "名字" in temp :
        ans[i].send_keys(information['name'])
    elif "班" in temp:
        ans[i].send_keys(information['class'])
    elif "机" in temp or "电话" in temp or "联" in temp:
        ans[i].send_keys(information['tel'])
    elif "学号"  in temp:
        ans[i].send_keys(information['stuid'])
    elif "QQ" in temp or "qq" in temp:
        ans[i].send_keys(information['qq'])
    elif "性别" in temp:
        ans[i].send_keys(information['sex'])
    else:
        continue

#如果需要自己补充一些信息的话直接将下面的语句注释掉即可
driver.find_element_by_class_name('published-form__footer-buttons').click()      #提交

time.sleep(200)   #保证浏览器一段时间内不关闭