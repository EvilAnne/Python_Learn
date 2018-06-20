#!/usr/bin/python
# -*- encoding:utf-8 -*-
# 获取FOFA IP 列表
#只能获取1万条；后面需要钱；凉凉〜〜

import json
import sys
import os
import requests
from multiprocessing import Process
from base64 import b64encode

def main():
	Lookup_type = sys.argv[1]
	save_file_name = 'ip_list.txt'
	for p in range(1,99):
		encode_bytes = bytes(Lookup_type,encoding='utf-8')
		encode = b64encode(encode_bytes)
		results_json = "https://fofa.so/api/v1/search/all?email=XXX@126.com&key=XXX&qbase64={}&page={}&size=1000&country=KZ".format(str(encode,'utf-8'),p)
		res = requests.get(results_json)
		try:
			json_res = res.text
			data = json.loads(json_res)
			results = data['results']
			query = data['query']
			for x in results:
				ip_list,*_ = x
				with open(save_file_name,'a') as fd:
					fd.writelines(ip_list + '\n')
					print(ip_list)
			numberlen = len(open(save_file_name, 'r').readlines())
			print('Number:{}   {}'.format(numberlen, query))
		except:
			break

if __name__ == '__main__':
	p = Process(target=main)
	p.start()