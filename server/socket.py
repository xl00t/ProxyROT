from http_parser.parser import HttpParser as Http_Parser

'''
['__class__', '__delattr__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__setstate__', '__sizeof__', '__str__', '__subclasshook__', 'execute', 'get_errno', 'get_fragment', 'get_headers', 'get_method', 'get_path', 'get_query_string', 'get_status_code', 'get_url', 'get_version', 'get_wsgi_environ', 'is_chunked', 'is_headers_complete', 'is_message_begin', 'is_message_complete', 'is_partial_body', 'is_upgrade', 'maybe_parse_url', 'recv_body', 'recv_body_into', 'should_keep_alive']
'''


class HttpParser:
    def __init__(self, raw_http):
        self.raw_http = raw_http
        self.parser = Http_Parser()
        self.parsed_obj = self.Parse_data()
        self.headers = self.parsed_obj.get_headers()
        self.method = self.parsed_obj.get_method()
        self.path = self.parsed_obj.get_path()
        self.url = self.parsed_obj.get_url()
        self.body = self.parsed_obj.recv_body()
        

    def Parse_data(self):
        self.parser.execute(self.raw_http, len(self.raw_http))
        return self.parser
        
