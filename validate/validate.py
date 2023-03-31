import requests
import threading
from server.proxy import *

TEST_URLS = [
    "http://ifconfig.me/"
]


class ValidateHTTPProxies:
    def __init__(self, file, out_name='',  threads=20):
        self.threads = threads
        self.proxy_file = file
        self.proxy_file_name = self.proxy_file.name
        self.out_proxy_file_name = f"alive_{self.proxy_file_name}" if out_name == '' else out_name
        self.proxies = Proxies(self.proxy_file).proxy_list
        self.alive_proxies = self.Test_Proxies(self.proxies)
        self.Save_Alive()
    
    def Test_Proxies(self, proxies):
        thread_array = []
        retval = [None for i in range(len(proxies))]
        for j in range(0, len(proxies), self.threads):
            for i in range(self.threads):
                thread = threading.Thread(target=self.Test_Proxy, args=(proxies[j+i], retval, j+i))
                thread.start()
                thread_array.append(thread)
            
            for thread in thread_array:
                thread.join()
        
        return [alive for alive in retval if alive]

    def Test_Proxy(self, prox, return_val, i):
        url = TEST_URLS[0]
        proxy = prox.Proxy_To_dict()
        try:
            r = requests.get(url, proxies=proxy, timeout=1).text.replace('\n','')
            if prox.ip == r:
                print(prox.ip, r)
                return_val[i] = prox
            else:
                return_val[i] = False 
        except Exception as e:
            return_val[i] = False

    def Save_Alive(self, filename="data/alive_proxy_list.txt"):
        file = open(filename, 'w')
        proxy_list_string = ""
        for proxy in self.alive_proxies:
            proxy_list_string += f"{proxy.scheme}://{proxy.ip}:{proxy.port}\n"
        
        file.write(proxy_list_string)
        file.close()