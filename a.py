# File Name: spider_threading.py
import os
import time
import threading
import socket
import ssl
from urllib.parse import urlparse
import qq

# 需要爬取图片的地址列表
urls = qq.result



# 定义一个爬虫类
class Crawler(threading.Thread):
    def __init__(self, url):
        threading.Thread.__init__(self)
        self.url = url
        self.response = b''

    def run(self):
        # urlparse 方法用来处理 URL ，其返回值便于获得域名和路径
        url = urlparse(self.url)
        # 创建 socket 实例
        user = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18363'
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ss = ssl.create_default_context().wrap_socket(self.sock, server_hostname= url.netloc)


        self.ss.connect((url.netloc, 443))

        print('连接成功', url.path)
        # 向服务器发送的数据的固定格式
        data = 'GET {} HTTP/1.1\r\nHost: {}\r\nUser-Agent: {}\r\nConnection: close\r\n\r\n'.format(
            url.path, url.netloc, user)
        # 向服务器发送数据，阻塞运行
        self.ss.send(data.encode())
        # 接收服务器返回的数据，阻塞运行
        while True:
            # 每次接收 1K 数据
            d = self.ss.recv(1024)
            if d:
                self.response += d
            else:
                break
        print('接收数据成功', url.path)
        name = url.path[-7:-1]
        print(name)
        f = open(name +'g' , 'wb')
        f.write(self.response.split(b'\r\n\r\n')[1])
        f.close()
        print('保存文件成功', url.path)
        self.sock.close()

def main():
    start = time.time()
    crawler_list = []
    for url in urls:
        # 创建爬虫实例
        crawler = Crawler(url)
        crawler_list.append(crawler)
        # 开始爬取数据
        crawler.start()
    # 将主线程挂起，直到全部子线程内的爬虫程序运行完毕
    for crawler in crawler_list:
        crawler.join()
    print('耗时：{:.2f}s'.format(time.time() - start))

if __name__ == '__main__':
    main()
