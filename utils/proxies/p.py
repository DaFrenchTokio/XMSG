import os,sys,json
import re,random,requests
import threading,_thread,time

temp = os.getenv("temp") + "\\SBPROXIES"

def scrape():
    proxieslog = []
    def fetch(url, custom_regex):
        global proxylist
        try: 
            proxylist = requests.get(url, timeout=5).text
        except Exception: 
            pass
        finally:
            proxylist = proxylist.replace('null', '')
        custom_regex = custom_regex.replace('%ip%', '([0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3})')
        custom_regex = custom_regex.replace('%port%', '([0-9]{1,5})')
        for proxy in re.findall(re.compile(custom_regex), proxylist):
            proxieslog.append(f"{proxy[0]}:{proxy[1]}")

    sources = [
        ["http://spys.me/proxy.txt", "%ip%:%port% "],
        ["http://www.httptunnel.ge/ProxyListForFree.aspx", " target=\"_new\">%ip%:%port%</a>"],
        ["https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/proxies.json",
            "\"ip\":\"%ip%\",\"port\":\"%port%\","],
        ["https://raw.githubusercontent.com/fate0/proxylist/master/proxy.list",
            '"host": "%ip%".*?"country": "(.*?){2}",.*?"port": %port%'],
        ["https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list.txt",
            '%ip%:%port% (.*?){2}-.-S \\+'],
        ["https://raw.githubusercontent.com/opsxcq/proxy-list/master/list.txt",
            '%ip%", "type": "http", "port": %port%'],
        ["https://www.us-proxy.org/",
            "<tr><td>%ip%<\\/td><td>%port%<\\/td><td>(.*?){2}<\\/td><td class='hm'>.*?<\\/td><td>.*?<\\/td><td class='hm'>.*?<\\/td><td class='hx'>(.*?)<\\/td><td class='hm'>.*?<\\/td><\\/tr>"],
        ["https://free-proxy-list.net/",
            "<tr><td>%ip%<\\/td><td>%port%<\\/td><td>(.*?){2}<\\/td><td class='hm'>.*?<\\/td><td>.*?<\\/td><td class='hm'>.*?<\\/td><td class='hx'>(.*?)<\\/td><td class='hm'>.*?<\\/td><\\/tr>"],
        ["https://www.sslproxies.org/",
            "<tr><td>%ip%<\\/td><td>%port%<\\/td><td>(.*?){2}<\\/td><td class='hm'>.*?<\\/td><td>.*?<\\/td><td class='hm'>.*?<\\/td><td class='hx'>(.*?)<\\/td><td class='hm'>.*?<\\/td><\\/tr>"],
        [
            "https://api.proxyscrape.com/?request=getproxies&proxytype=http&timeout=6000&country=all&ssl=yes&anonymity=all",
            "%ip%:%port%"],
        ["https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt", "%ip%:%port%"],
        ["https://raw.githubusercontent.com/shiftytr/proxy-list/master/proxy.txt", "%ip%:%port%"],
        ["https://proxylist.icu/proxy/", "<td>%ip%:%port%</td><td>http<"],
        ["https://proxylist.icu/proxy/1", "<td>%ip%:%port%</td><td>http<"],
        ["https://proxylist.icu/proxy/2", "<td>%ip%:%port%</td><td>http<"],
        ["https://proxylist.icu/proxy/3", "<td>%ip%:%port%</td><td>http<"],
        ["https://proxylist.icu/proxy/4", "<td>%ip%:%port%</td><td>http<"],
        ["https://proxylist.icu/proxy/5", "<td>%ip%:%port%</td><td>http<"],
        ["https://www.hide-my-ip.com/proxylist.shtml", '"i":"%ip%","p":"%port%",'],
        ["https://raw.githubusercontent.com/scidam/proxy-list/master/proxy.json",
            '"ip": "%ip%",\n.*?"port": "%port%",']
    ]
    threads = []
    for url in sources:
        # send them out in threads
        t = threading.Thread(target=fetch, args=(url[0], url[1]))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()

    proxies = list(set(proxieslog))
    with open(temp, "w") as f:
        for proxy in proxies:
            for i in range(random.randint(7, 10)):
                f.write(f"{proxy}\n")

def get():
    if os.stat(temp).st_size == 0:
        scrape()
    proxies = open(temp).read().split('\n')
    proxy = proxies[0]
    with open(temp, 'r+') as fp:
        lines = fp.readlines()
        fp.seek(0)
        fp.truncate()
        fp.writelines(lines[1:])
    return proxy