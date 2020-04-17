import nmap
nm = nmap.PortScanner()
nm.scan(hosts='192.168.1.0/24', arguments='-n -sP -PE --min-hostgroup 1024 --min-parallelism 1024')
print(nm.all_hosts())