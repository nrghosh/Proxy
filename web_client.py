#!/usr/bin/python3
#
# Wesleyan University
# COMP 332, Spring 2018
# Homework 3: Simple web client to interact with proxy
#
# Example usage:
#
#   python3 web_client.py <proxy_host> <proxy_port> <requested_url>
#
# Nikhil Ghosh

# Python modules
import binascii
import socket
import sys

# Project modules
import http_util

class WebClient:

    def __init__(self, proxy_host, proxy_port, url):
        self.proxy_host = proxy_host
        self.proxy_port = proxy_port
        self.url = url
        self.start()

    def start(self):

        # Open connection to proxy
        try:
            proxy_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            proxy_sock.connect((self.proxy_host, self.proxy_port))
            print("Connected to socket")
        except OSError as e:
            print("Unable to connect to socket: ", message)
            if proxy_sock:
                proxy_sock.close()
            sys.exit(1)

        # Send requested URL to proxy
        str_url = self.url
        [hostname, pathname] = http_util.parse_url(str_url)
        str_req = http_util.create_http_req(hostname, pathname)
        bin_req = str_req.encode('utf-8')
        proxy_sock.sendall(bin_req)

        # Receive binary data from proxy
        bin_reply = b''
        while True:
            more = proxy_sock.recv(4096)
            if not more:
                break
            bin_reply += more
        print('Client received from proxy (showing 1st 300 bytes): ', bin_reply)
        
        # Close connection to proxy
        proxy_sock.close()

def main():

    print (sys.argv, len(sys.argv))
    proxy_host = 'localhost'
    proxy_port = 50007

# NOTE: If a date is not found, it will not be cached (you'll keep getting 200 OK responses)
    url = str(input("Please enter URL: "))

    if len(sys.argv) > 1:
        proxy_host = sys.argv[1]
        proxy_port = int(sys.argv[2])
        url = sys.argv[3]

    web_client = WebClient(proxy_host, proxy_port, url)

if __name__ == '__main__':
    main()
