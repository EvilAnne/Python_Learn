import os
import threading

def rsync_Vuln_Check(ip):
	ip = ip.strip()
	command = "rsync " + ip+"::"
	print("Checking {}".format(ip))
	dirlist = []
	for line in os.popen(command):
		x = line.find("\t")
		y = line[0:x - 6]
		dirlist.append(y)

	for dir in dirlist:
		userlist = ["test", "root", "www"]
		for user in userlist:
			command = "rsync " + user + "@" + ip + "::" + dir + " --password-file=pass.txt"
			try:
				#print(command)
				output = os.system(command)
				if os.popen(command).read():
					res_str = "[+]Vul Found： " + command
					with open("Vuln_IP.txt","a+") as f:
						f.write(res_str+"\n")
				else:
					pass
			except Exception as e:
				print(e)


with open('ip.txt') as f:
	iplist = f.readlines()
	for x in iplist:
		rsync_Vuln_Check(x)



