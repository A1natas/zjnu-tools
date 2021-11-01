import requests
import json
import os

#在此处输入配置即可使用

url="192.168.1.1"       #路由器网关url，openwrt一般是10.0.0.1，也有192.168.1.1的

passwd=""               #路由器管理密码，openwrt默认应该是password（看固件作者）

yidongusername=""       #移动账号，默认应该是jhwcl+手机后八位

yidongpassword=""       #移动密码，默认应该是手机后六位或者是六位数生日或者是123456

yidongservice=""        #移动服务名，杏园应该是这个东西：JHDY-GSXY-MX960-1

dianxinusername=""      #电信账号，找营业厅看

dianxinservice=""       #电信服务名，闪讯一般留空即可

#电信密码由于经常换，在程序内输入即可


#获取id内容
def get(id):
    url1='http://'+url+'/cgi-bin/luci/rpc/uci?auth='+token
    
    getid={
    "method":"get",
    "params":["network", "wan", id],
    }

    getitem=json.loads(requests.post(url1,data=json.dumps(getid)).text)['result']

    return getitem

#获取所有信息
def getall():
    username=get('username')
    password=get('password')
    service=get('service')

    print("username:"+str(username))
    print("password:"+str(password))
    print("service:"+str(service))

#设置id内容
def set(id,content):
    url1='http://'+url+'/cgi-bin/luci/rpc/uci?auth='+token

    setid={
        "method":"set",
        "params":["network","wan",id,content]
    }

    setitem=json.loads(requests.post(url1,data=json.dumps(setid)).text)['result']

    return setitem

#设置成移动网
def yidong():
    result1=set("username",yidongusername)
    result2=set("password",yidongpassword)
    result3=set("service",yidongservice)

    if(result1 and result2 and result3):
        print("set success")
    else:
        print('error,set again')

#设置成电信网
def dianxin(id):
    result1=set("username",dianxinusername)
    result2=set("password",id)
    result3=set("service",dianxinservice)

    if(result1 and result2 and result3):
        print("set success")
    else:
        print('error,set again')
#重启wan网口（断网的时候用，排除路由器问题）
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
#提交所有设置
def commitsettings():
    url1='http://'+url+'/cgi-bin/luci/rpc/uci?auth='+token

    commit={
        "method":"commit",
        "params":["network"]
    }

    commitresult=json.loads(requests.post(url1,data=json.dumps(commit)).text)['result']

    return commitresult
#菜单
def menu():
    print("1.电信改密码")
    print("2.改移动网（晚上断网）")
    print("3.重启网络（掉线的时候用）")
    print("4.获取当前账号密码状态")
    print("5.退出")

#获取token
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
