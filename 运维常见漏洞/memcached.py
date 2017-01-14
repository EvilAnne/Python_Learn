import threading
import argparse
import sys
from socket import *



#连接memcached 端口默认为11211
def Connect_Memcached(tarHost,tarPort):
	try:
		setdefaulttimeout(5)
		s = socket(AF_INET,SOCK_STREAM)
		s.connect((tarHost,tarPort))
		s.send(b'stats\r\n')
		result = s.recv(4096)
		print("\033[1;31;40m [+] {}:{} unauthorized Access \033[0m".format(tarHost,tarPort))
	except:
		print(" [-] {}:{} unauthorized reject".format(tarHost,tarPort))



def IP_C(tarHost,tarPort):
	for x in range(0,254):
		iplist = '{}.{}'.format(tarHost, x)
		#Connect_Memcached(iplist,tarPort)
		t = threading.Thread(target=Connect_Memcached,args=(iplist,tarPort))
		t.start()



print('python {} Default Port 11211 只需要输入C段地址'.format(sys.argv[0]))
tarHost = input("Input IP 192.168.0：")
tarPort = 11211
IP_C(tarHost,tarPort)