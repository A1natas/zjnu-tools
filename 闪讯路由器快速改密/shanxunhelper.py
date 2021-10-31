import requests
import json
import os

#�ڴ˴��������ü���ʹ��

url="192.168.1.1"       #·��������url

passwd=""               #·������������

yidongusername=""       #�ƶ��˺�

yidongpassword=""       #�ƶ�����

yidongservice=""        #�ƶ�������

dianxinusername=""      #�����˺�

dianxinservice=""       #���ŷ���������Ѷһ�����ռ���

#�����������ھ��������ڳ��������뼴��


#��ȡid����
def get(id):
    url1='http://'+url+'/cgi-bin/luci/rpc/uci?auth='+token
    
    getid={
    "method":"get",
    "params":["network", "wan", id],
    }

    getitem=json.loads(requests.post(url1,data=json.dumps(getid)).text)['result']

    return getitem

#��ȡ������Ϣ
def getall():
    username=get('username')
    password=get('password')
    service=get('service')

    print("username:"+str(username))
    print("password:"+str(password))
    print("service:"+str(service))

#����id����
def set(id,content):
    url1='http://'+url+'/cgi-bin/luci/rpc/uci?auth='+token

    setid={
        "method":"set",
        "params":["network","wan",id,content]
    }

    setitem=json.loads(requests.post(url1,data=json.dumps(setid)).text)['result']

    return setitem

#���ó��ƶ���
def yidong():
    result1=set("username",yidongusername)
    result2=set("password",yidongpassword)
    result3=set("service",yidongservice)

    if(result1 and result2 and result3):
        print("set success")
    else:
        print('error,set again')

#���óɵ�����
def dianxin(id):
    result1=set("username",dianxinusername)
    result2=set("password",id)
    result3=set("service",dianxinservice)

    if(result1 and result2 and result3):
        print("set success")
    else:
        print('error,set again')
#����wan���ڣ�������ʱ���ã��ų�·�������⣩
def restartwan():
    url2='http://'+url+'/cgi-bin/luci/rpc/sys?auth='+token

    restartwan={
        "method":"exec",
        "params":["/sbin/ifup wan"]
    }

    re=json.loads(requests.post(url2,data=json.dumps(restartwan)).text)['result']

    if(re==''):
        print("Reboot success")
    else:
        print("Reboot failed")
#�ύ��������
def commitsettings():
    url1='http://'+url+'/cgi-bin/luci/rpc/uci?auth='+token

    commit={
        "method":"commit",
        "params":["network"]
    }

    commitresult=json.loads(requests.post(url1,data=json.dumps(commit)).text)['result']

    return commitresult
#�˵�
def menu():
    print("1.���Ÿ�����")
    print("2.���ƶ��������϶�����")
    print("3.�������磨���ߵ�ʱ���ã�")
    print("4.��ȡ��ǰ�˺�����״̬")
    print("5.�˳�")

#��ȡtoken
url0 = 'http://'+url+'/cgi-bin/luci/rpc/auth'

data = {
    "method":"login",
    "params":["root",passwd]
}

token = json.loads(requests.post(url0,data=json.dumps(data)).text)['result']

#print(token)
while(True):
    menu()
    id=input("input your id:")
    if(id==1):
        password=input("input your password:")
        dianxin(password)
        result=commitsettings()
        print(result)
        restartwan()

    elif(id==2):
        yidong()
        result=commitsettings()
        print(result)
        restartwan()

    elif(id==3):
        restartwan()

    elif(id==4):
        getall()

    elif(id==5):
        break
    
    else:
        print("wrong")
        continue

#Xunflash
