from socket import *
import argparse
import threading

def connectHost(tarHost,tarPort):
	try:
		s = socket(AF_INET,SOCK_STREAM)
		s.connect((tarHost,tarPort))
		s.send(b'Python Test\r\n')
		result = s.recv(1024)
		print(" [+] {}/tcp open".format(tarPort))
		print(" [+] Banner Info: {}".format(result))
	except:
		print(" [-] {}/tcp closed".format(tarPort))



def ScanPort(tarHost,tarPort):
	try:
		tarIP = gethostbyname(tarHost)
	except:
		print(" [-] Unknown Host {}".format(tarHost[0]))

	try:
		tarName = gethostbyaddr(tarIP)
	except:
		print(" [-] Unknown Host Name {}".format(tarIP))

	for x in tarPort:
		print("Port Scan {}".format(int(x)))
		t = threading.Thread(target=connectHost,args=(tarHost,int(x)))
		t.start()


def main():
	p = argparse.ArgumentParser(usage='''Python ScanPort.py -host 127.0.0.1 -port 21,22,23''',description="Python Port Scan")
	p.add_argument('-host',help='Load IP Address')
	p.add_argument('-port',help='Load Port')
	args = p.parse_args()
	tarHost = args.host
	tarPort = args.port
	if tarPort == 'all':
		tarPort = '21,22,23,25,53,80,110,139,143,389,443,445,465,873,993,995,1080,1723,1433,1521,3306,3389,3690,5432,5800,5900,6379,7001,8000,8001,8080,8081,8888,9200,9300,9080,9999,11211,27017'
		tarPort = str(tarPort).split(',')
		ScanPort(tarHost,tarPort)
	else:
		tarPort = str(args.port).split(',')
		ScanPort(tarHost,tarPort)


if __name__ == '__main__':
	main()