import requests
from bs4 import BeautifulSoup
import os
import re

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1'
          
}
url = 'http://923yzq.com/newslist/45/index-2.html?236787987'
html = requests.get(url, headers=headers)
result = re.findall(r'/news/(\d+).html', html.text)
for i in result:
    url = 'http://923yzq.com/news/' + i +'.html?236787987'
    html = requests.get(url, headers=headers)
    result = re.findall(r'<img src="(.+?)"></p>', html.text)
   