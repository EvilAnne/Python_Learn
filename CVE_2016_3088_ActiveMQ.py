#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
import re
import sys
import datetime
import threading
import requests
import argparse
from socket import *
from urllib.parse import urlsplit
#from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

#端口开放保存文件
def save_file(filename,Intranet):
	create_file_name = datetime.datetime.now().strftime('%Y-%m-%d')
	new_file = '{}_port_{}'.format(filename,create_file_name)
	with open(new_file,'a') as fd:
		fd.writelines(Intranet + '\n')


#socket请求
def socket_request(tarip,tarport):
	try:
		timeout = 2
		setdefaulttimeout(timeout)
		s = socket(AF_INET, SOCK_STREAM)
		address = (str(tarip),int(tarport))
		s.connect(address)
		s.close()
		info = '{}:{}'.format(tarip, tarport)
		print('\033[6;30;42m' + info + '\033[0m')
		yield info
	except:
		print('\033[0;31m' + '{}:{} {}'.format(tarip,tarport,'Close') + '\033[0m')

#判断是单个还是批量;
def Target_classification(target:str) -> str:
	port_list = ['8161','61616']
	if file.startswith('http://') or file.startswith('https://'):
		ip = urlsplit(target).netloc
		for port in port_list:
			socket_request(ip,int(port))
	else:
		if os.path.isfile(file):
			with open(file,'r') as read_ip:
				for ip in read_ip:
					for port in port_list:
						target_ip = ip.strip()
						target_port = int(port)
						for Intranet in socket_request(target_ip,target_port):
							save_file(file,Intranet)
		else:
			print("File does not exist!!!")


#http://192.168.1.69:8161/
#登录状态;
def ActiveMQ_admin(file:str) -> str:
	headers = {
		'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5376e Safari/8536.25',
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
		'Accept-Encoding': 'gzip, deflate, sdch',
		'Authorization': 'Basic YWRtaW46YWRtaW4=',  #admin:admin
		'Accept-Language': 'zh-CN,zh;q=0.8'
	}

	with open(file,'r') as fd:
		for ip in fd:
			try:
				ip_http = 'http://{}/admin/test/systemProperties.jsp'.format(''.join(ip.split()))
				response = requests.get(ip_http,headers=headers,timeout=2)
				print('\033[6;30;42m' + '{}  --> {}'.format(ip_http,response.status_code) + '\033[0m')
				save_file('admin',ip_http)
			except:
				print('\033[0;31m' + '{}'.format(ip_http, 'Close') + '\033[0m')


def main():
	print("""
python {name} -f ip.txt  批量验证端口是否有开放然后保存在文本中
python {name} -r ip.txt  批量验证弱口令
	""".format(name=sys.argv[0]))
	parser = argparse.ArgumentParser(description="ActiveMQ CVE-2016-3088 Scan Script.")
	parser.add_argument('-f','--file',help='To determine whether there is open port',nargs='?')
	parser.add_argument('-d','--depth',help='Blasting HTTP basic authentication',nargs='?')
	args = parser.parse_args()
	file = args.file
	depth = args.depth
	if file:
		pool = ThreadPoolExecutor(10)
		t = pool.submit(Target_classification, file)
		t.result()
	elif depth:
		pool = ThreadPoolExecutor(10)
		t = pool.submit(ActiveMQ_admin, file)
		t.result()





if __name__ == '__main__':
    main()