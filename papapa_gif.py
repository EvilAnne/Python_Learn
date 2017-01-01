import requests
import threading
import lxml
import re
import urllib
import sys
import time
import random
import urllib.request
from bs4 import BeautifulSoup


#获取文件gif路私
def get_image_src(url):
        headers = {
                'Host': 'www.lovefou.com',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:47.0) Gecko/20100101 Firefox/47.0',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3'
        }

        r = requests.get(url=url,headers=headers)

        soup = BeautifulSoup(r.content,'lxml')

        div_str = soup.find_all(name='div',attrs={'class':'dongtai'})

        re_div_str = str(div_str)

        s = BeautifulSoup(re_div_str,'lxml')
        for link_src in s.find_all(name='img'):
            get_download_src = link_src.get('src')
            print(type(get_download_src))



#多线程
urls = []
threads = []

for i in range(0,10):
    for x in range(0,10):
        for v in range(0,10):
            html_url = 'http://www.lovefou.com/dongtaitu/47{}{}{}.html'.format(i,x,v)
            urls.append(html_url)



thread_count = len(urls)

for i in range(thread_count):
    t = threading.Thread(target=get_image_src,args=(urls[i],))
    threads.append(t)


for i in range(thread_count):
    threads[i].start()
