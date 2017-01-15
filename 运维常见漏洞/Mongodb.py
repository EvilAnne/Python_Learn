import pymongo
import threading
import argparse
from socket import *


def connect_Host(tarHost,tarPort):
	try:
		setdefaulttimeout(3)
		s = socket(AF_INET,SOCK_STREAM)
		s.connect((tarHost,tarPort))
		print("{}:{} Open".format(tarHost,tarPort))
		s.close()
		return True
	except:
		print("{}:{} Closed".format(tarHost,tarPort))
		return False


def Access_Mongodb(tarHost,tarPort):
	result = connect_Host(tarHost,tarPort)
	if result:
		conn = pymongo.MongoClient(tarHost,tarPort,socketTimeoutMS=2000)
		dbs = conn.database_names()
		result = "\033[1;31;40m {}:{} -> Data: {} \033[0m".format(tarHost,tarPort,dbs)
		print(result)
		with open("Seccued.txt","a+") as f:
			f.write(result)
	else:
		pass


#C段
def IP_C(tarHost,tarPort):
	for x in range(0,254):
		iplist = '{}.{}'.format(tarHost, x)
		t = threading.Thread(target=Access_Mongodb,args=(iplist,tarPort))
		t.start()


def main():
	p = argparse.ArgumentParser(usage='python Mongodb.py --host 192.168.4 --port 27017',description='Mongodb unauthorized reject')
	p.add_argument('--host',help='输入C段 如：192.168.0',type=str)
	p.add_argument('--port',help='输入端口：27017',type=int)
	args = p.parse_args()
	tarHost = args.host
	tarPort = args.port
	IP_C(tarHost,tarPort)

if __name__ == '__main__':
    main()