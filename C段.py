import threading,sys
import queue
import re
import nmap
import requests
class V1(threading.Thread):
    def __init__(self,q):
        threading.Thread.__init__(self)
        self._queue = q
    def run(self):
        while not self._queue.empty():

            ip = self._queue.get(timeout=0.5)
            self.url = 'http://' + ip

            self.headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1'
          
}
            try:
                r = requests.get(self.url, headers=self.headers, timeout=5)
                r.encoding = 'utf-8'
                content = r.text
                status = r.status_code
                title = re.search(r'<title>(.*)</title>', content)

                if title:
                    title = title.group(1).strip().strip("\r").strip("\n")[:15]
                else:
                    title = "None"
 
                banner = 'Not Found'
                try:
                    banner = r.headers['Server'][:20]
                except:
                    pass
 
                sys.stdout.write("http://%-16s %-6s %-26s %-30s\n" % (ip, status, banner, title))
 
            except:

                pass
def main():
    nm = nmap.PortScanner()
    nm.scan(hosts='104.203.57.212/24', arguments='-n -sP -PE --min-hostgroup 1024 --min-parallelism 1024')
    work = nm.all_hosts()
    thread_count = 5
    threads = []
    q = queue.Queue()
 
    for i in work:
        q.put(i)

    for i in range(thread_count):
        threads.append(V1(q))
    
    for t in threads:
        t.start()
    for t in threads:
        t.join()
 
if __name__ == '__main__':
    main()