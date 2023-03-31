from urllib.parse import urlparse
from random import randint


class Proxy:
    def __init__(self, proxy_str):
        self.scheme = None
        self.ip = None
        self.port = None 
        self.Parse_Proxy(proxy_str)

    def Parse_Proxy(self, proxy_str):
        try:
            url_parsed = urlparse(proxy_str)
            self.ip, port = url_parsed.netloc.split(':')
            self.port = int(port)
            self.scheme = url_parsed.scheme
        except:
            pass
    
    def Proxy_To_dict(self):
        proxy_str = f"{self.scheme}://{self.ip}:{self.port}"
        proxy_obj = {self.scheme: proxy_str}
        return proxy_obj

class Proxies:
    def __init__(self, proxies_file="data/proxy_list.txt"):
        self.proxies_file = proxies_file
        self.proxy_list = self.ParseProxyFile(proxies_file)

    def ParseProxyFile(self, proxies_file):
        if type(proxies_file) == str:
            proxy_f =  open(proxies_file, 'r').read().splitlines()
        else:
            proxy_f =  proxies_file.read().splitlines()

        proxies = []
        for proxy in proxy_f:
            proxies.append(Proxy(proxy))

        return proxies
    
    def ChooseRandomProxy(self):
        return self.proxy_list[randint(0, len(self.proxy_list)-1)]

