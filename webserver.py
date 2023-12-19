"""
Implement an HTTP web server in Python that knows how to run server-side
CGI scripts coded in Python;  serves files and scripts from current working
dir;  Python scripts must be stored in webdir\cgi-bin or webdir\htbin;
"""

import os, sys
from http.server import HTTPServer, CGIHTTPRequestHandler

webdir = '.'   # where your html files and cgi-bin script directory live
port   = 80    # default http://localhost/, else use http://localhost:xxxx/

# This command changes the current working directory to webdir, which is the directory where this file is saved
os.chdir(webdir)
#  This variable has the hostname and portnumber
srvraddr = ("", port)
#  srvrobj stores our HTTPServer object with srvraddr and CGIHTTPRequestHandler passed to it:  One class, HTTPServer, is a socketserver.TCPServer subclass. It creates and listens at the HTTP socket, dispatching the requests to a handler (CGIHTTPRequestHandler in this case, which looks at the folder structure and runs any CGI scripts in cgi-bin directory)
srvrobj  = HTTPServer(srvraddr, CGIHTTPRequestHandler)
srvrobj.serve_forever()                                # run as perpetual daemon
