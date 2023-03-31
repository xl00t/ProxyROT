#!/usr/bin/env python3
import traceback
import socket, sys
import threading
import requests
import server.dump as dump
from server.proxy import Proxies
from server.socket import HttpParser

BUFFER_SIZE = 8192
BACK_LOG = 50

class HTTPProxyServer:
    def __init__(self, ip, port, proxy):
        self.ip = ip
        self.port = port
        self.proxy_list = proxy

    def Start_Server(self):
        try:
            Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            Socket.bind((self.ip,self.port))
            Socket.listen(BACK_LOG)
            i=1
            threads = []
            while 1:
                conn, addr = Socket.accept()
                thread = threading.Thread(target=self.Forward_Request, args=(conn, addr,i))
                threads.append(thread)
                thread.start()
                i+=1

        except KeyboardInterrupt:
            if Socket:
                Socket.close()

            print("[?] KeyboardInterrupt (CTRL+C)")
            sys.exit(1)
        except socket.error as Message:
            if Socket:
                Socket.close()
            print("[-] Could Not Open Socket:", Message)
            sys.exit(1)
        except Exception as Error:
            print("[-] Error : ", Error)
            sys.exit(1)
    
    def Forward_Request(self, conn, addr, i):
        data = conn.recv(BUFFER_SIZE)
        # print(data)
        http = HttpParser(data)
        req = requests.Request(method=http.method, url=http.url, headers=http.headers, data=http.body)
        r = req.prepare()
        s = requests.Session()

        result = False
        retries = 5
        list_prox = Proxies(self.proxy_list)
        while retries:
            try:
                chosed_prox = list_prox.ChooseRandomProxy()
                proxy_obj = chosed_prox.Proxy_To_dict()
                result = s.send(r, allow_redirects=False, proxies=proxy_obj, timeout=5)
                if result:
                    print(f"{http.method} {http.url} via {chosed_prox.scheme}://{chosed_prox.ip}:{chosed_prox.port} sucess")
                    break
            except Exception as e:
                #print(f"Error with {proxy_obj} {http.url} via {http.url} sucess")
                retries -= 1
        data = dump.dump_response(result, request_prefix='', response_prefix='')
        conn.send(data)

        return True


'''
['CONTENT_DECODERS', 'REDIRECT_STATUSES', '__abstractmethods__', '__class__', '__del__', '__delattr__', '__dict__', '__dir__', '__doc__', '__enter__', '__eq__', '__exit__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__iter__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__next__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '_abc_impl', '_body', '_checkClosed', '_checkReadable', '_checkSeekable', '_checkWritable', '_connection', '_decode', '_decoder', '_error_catcher', '_flush_decoder', 
'_fp', '_fp_bytes_read', '_handle_chunk', '_init_decoder', '_init_length', '_original_response', '_pool', '_request_url', '_update_chunk_length', 'chunk_left', 'chunked', 'close', 'closed', 'connection', 'data', 'decode_content', 'enforce_content_length', 'fileno', 'flush', 'from_httplib', 'get_redirect_location', 'getheader', 'getheaders', 'geturl', 'headers', 'info', 
'isatty', 'isclosed', 'length_remaining', 'msg', 'read', 'read_chunked', 'readable', 'readinto', 'readline', 'readlines', 'reason', 'release_conn', 'retries', 'seek', 'seekable', 'status', 'stream', 'strict', 'supports_chunked_reads', 'tell', 'truncate', 'version', 'writable', 'writelines']
'''