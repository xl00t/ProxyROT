#!/usr/bin/env python3
import argparse
from server.server import HTTPProxyServer
from validate.validate import ValidateHTTPProxies

def main():
    parser = argparse.ArgumentParser(
        prog="ProxyRot",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description='This is a set of modules to manage rotative Proxy.',
        epilog='xl00t'
    )

    sub_parsers = parser.add_subparsers(
        title="Different modules",
        description="Select the module to use",
        dest="mode",
        required=True,
    )
    # sever module subparser
    parser_server = sub_parsers.add_parser("server", help="Server mode")
    parser_server.add_argument(
        "-i", "--ip", type=str, help="Ip address to attach to", default="localhost"
    )
    parser_server.add_argument(
        "-p", "--port",type=int, help="Port bind to", default=8080
    )

    parser_server.add_argument(
        "--proxy", type=str, help="Proxy File", default='data/proxy_list.txt', required=False
    )

    # validate module subparser
    parser_validate = sub_parsers.add_parser("validate", help="Validate mode")
    parser_validate.add_argument(
        "--file", '-f', type=argparse.FileType('r'), help="Proxies list", default="data/proxy_list.txt", required=False
    )

    parser_validate.add_argument(
        "--out", '-o', type=str, help="Out file", default='', required=False
    )

    


    args = parser.parse_args()

    if args.mode == "server":
        HTTP_Proxy_Server = HTTPProxyServer(args.ip, args.port, args.proxy)
        print(f"Listening on : http://{HTTP_Proxy_Server.ip}:{HTTP_Proxy_Server.port}")
        HTTP_Proxy_Server.Start_Server()

    if args.mode == "validate":
        Validate_Module = ValidateHTTPProxies(args.file, args.out, threads=20)
    


if __name__ == '__main__':
    main()