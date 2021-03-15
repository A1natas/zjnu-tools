# coding=utf-8
import time
import requests
import datetime
import os
import logging
import sys
if sys.getdefaultencoding() != 'utf-8':
    reload(sys)
    sys.setdefaultencoding('utf-8')
# 需要搭配定时任务使用


FILE = os.getcwd()
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(filename=os.path.join(FILE,'log.txt'),level=logging.INFO, format=LOG_FORMAT)

def main():
    data_zyt = "__EVENTTARGET=btn_save&__EVENTARGUMENT=&__VIEWSTATE=%2FwEPDwUKMTg3NDMxMDU4M2Rki5huN92EcNRRN7X1sVr0aCbrtcXkrfJl4HmNWNFFw%2Fk%3D&__VIEWSTATEGENERATOR=3674067D&__EVENTVALIDATION=%2FwEdABc5MxuMpry7ULDVBzGGbkkinPdgn5d6iO4LuTjGeN2JM3llOAzR6kycDzMfToHX0QOa6jYEaUq7hqoikcwmGDr%2FnmnPxOBQ7q1ly%2B%2BofgUcfBMeg5WVSSvtrjLjx3x5POv400VKLRNp%2Fk6261iHtmxhYdp8PLLcr00Ykm6GIg%2FQPm2VAoUsguAjookCWDEX54sHQe9Pfyn7J2iyftT%2BCg0mL0jfXWdOZUPTgbQHBDwymb6wlsA0YdypgcCl8awhDxBgYuHAmLDqwPtQh9HDEtJjr%2Bc7NEwFf3c5FPeYdSyrXrYIOfZQS7Mh8jWxQ%2F3S2fHk%2FwGpGPyEyYtOtvQbZ7eyCWoEiO6Dd%2BV6RlHl9UDOJYVHlcFqi%2B%2BpsAvZk9q9RG5W1pRfvYYFhXg72yYOmnpySmm9X2U2t6Y11P%2BJ4lVyalm%2Bn0KUg6wbhm42RvKN577lL2zWcbD6zAaEib0znaI8tWsLH8H%2BNXQUYD4Kkws4BR73hBDFh5b%2BQ15kMx8hutDX9%2BLptw1D4IVe%2B4S61lC7&personname=%E4%BF%9E%E5%A4%A9%E7%BF%94&personcode=201831990538&txtCreateTime=" + datetime.datetime.now().strftime('%Y-%m-%d') + "&DATA_1=%E4%BD%93%E6%B8%A9%E6%AD%A3%E5%B8%B8&DATA_2=%E6%AD%A3%E5%B8%B8&DATA_3=%E4%BD%93%E6%B8%A9%E6%AD%A3%E5%B8%B8&DATA_4=%E5%90%A6&DATA_5=%E7%BB%BF%E7%A0%81&DATA_6=%E5%90%A6&DATA_7=%E5%90%A6&DATA_8=%E5%90%A6&DATA_9=%E5%90%A6&DATA_10=%E5%90%A6&DATA_11=&DATA_12=&DATA_13=%E6%B5%99%E6%B1%9F%E5%B8%88%E8%8C%83%E5%A4%A7%E5%AD%A6%E6%9C%AC%E9%83%A8%E6%A0%A1%E5%8C%BA&DATA_14=&DATA_15=%E6%88%91%E5%B7%B2%E7%9F%A5%E6%99%93%E5%B9%B6%E5%A6%82%E5%AE%9E%E5%A1%AB%E6%8A%A5&hidDATA_1=%E4%BD%93%E6%B8%A9%E6%AD%A3%E5%B8%B8&hidDATA_2=%E6%AD%A3%E5%B8%B8&hidDATA_3=%E4%BD%93%E6%B8%A9%E6%AD%A3%E5%B8%B8&hidDATA_4=%E5%90%A6&hidDATA_5=%E7%BB%BF%E7%A0%81&hidDATA_6=%E5%90%A6&hidDATA_7=%E5%90%A6&hidDATA_8=%E5%90%A6&hidDATA_9=%E5%90%A6&hidDATA_10=%E5%90%A6&hidDATA_11=&hidDATA_12=&hidDATA_13=%E6%B5%99%E6%B1%9F%E5%B8%88%E8%8C%83%E5%A4%A7%E5%AD%A6%E6%9C%AC%E9%83%A8%E6%A0%A1%E5%8C%BA&hidDATA_14=&hidDATA_15=%E6%88%91%E5%B7%B2%E7%9F%A5%E6%99%93%E5%B9%B6%E5%A6%82%E5%AE%9E%E5%A1%AB%E6%8A%A5"
    cookies_zyt = 'ASP.NET_SessionId=; yxkj_ticket=; LastUserCode='
    # 此 cookies 请自行抓包

    sign_res = sign_in(data_zyt,cookies_zyt)
    logging.info("开始提交")
    if sign_res != "":
        if sign_res.find("提交成功！已经返校师生，若腋下体温≥37.3℃，请到“体温填报”模块填写具体体温！")!=-1:
            logging.info("提交成功")

def sign_in(data,cookie):
    url = "http://zyt.zjnu.edu.cn/H5/ZJSFDX/CheckFillIn.aspx"
    url = "http://zyt.zjnu.edu.cn/H5/ZJSFDX/FillIn.aspx"
    try:
        headers = {
            "Cookie": cookie,
            "content-type": "application/x-www-form-urlencoded",
            "Referer": "http://zyt.zjnu.edu.cn/H5/ZJSFDX/FillIn.aspx"
        }
        response=requests.post(url,headers=headers,data=data,timeout=(2, 30))
        response.encoding = response.apparent_encoding
        return response.text
    except requests.exceptions.ReadTimeout:
        print("requests.exceptions.ReadTimeout:[%s]" % url)
        return ""
    except requests.exceptions.ConnectionError:
        print("requests.exceptions.ConnectionError:[%s]" % url)
        return ""

def str_time(pattern='%Y-%m-%d %H:%M:%S'):
    return time.strftime(pattern, time.localtime(time.time()))
if __name__ == "__main__":
    main()