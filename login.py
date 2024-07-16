import requests
from urllib.parse import urlsplit, quote
import re
import gzip


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36",
}

static_url = "http://www.msftconnecttest.com/redirect"

login_headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36",
    "Referer" : "",
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}

post_url = "http://172.16.128.139/eportal/InterFace.do?method=login"

post_data = {
    "userId=":"",
    "&password=":"",
    "&service=":"",
    "&queryString=":"",
    "&operatorPwd=&operatorUserId=&validcode=":"",
    "&passwordEncrypt=":"true",
}

def islogin() -> bool:
    url = "http://172.16.128.139/eportal/success.jsp"
    data = requests.get(url).content
    depressed_data = gzip.decompress(data=data)
    text = depressed_data.decode(encoding="gbk",errors="ignore")
    if text.find("登录成功") != -1:
        return True
    else:
        return False

def get_queryString() -> str:
    """
    获取queryString
    """
    static_res = requests.get(static_url, headers=headers)
    ans =  re.search(r"'(https?:\/\/[^\s'\"<>]+)'", static_res.text)
    redirct_url = ans.group(1)

    login_headers["Referer"] = redirct_url

    static_res_302 = urlsplit(redirct_url).query

    # url二次编码
    queryString = quote(quote(static_res_302))

    return queryString

if __name__=="__main__":

    if islogin():
        print("success")    
    else:
        queryString = get_queryString()
        post_data["&queryString="] = queryString
        # 账户
        post_data["userId="] = "wangpengwei21"
        # 密码
        post_data["&password="] = "wpw12138@"
        # 密码不加密
        post_data["&passwordEncrypt="] = "false"

        data =  "userId=" + post_data["userId="] +\
                "&password=" + post_data["&password="] + \
                "&queryString=" + post_data["&queryString="] + \
                "&service=" + post_data["&service="] + \
                "&operatorPwd=&operatorUserId=&validcode=" + post_data["&operatorPwd=&operatorUserId=&validcode="] + \
                "&passwordEncrypt=" + post_data["&passwordEncrypt="]


        res = requests.post(post_url, data=data,headers=login_headers)
        print(res.content.decode("utf8"))





