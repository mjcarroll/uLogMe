#!/usr/bin/env python3
# -*- coding: utf8 -*-
# ulogme_serve_https.py for https://github.com/Naereen/uLogMe/
# MIT Licensed, https://lbesson.mit-license.org/
#
"""
ulogme_serve_https.py - simple HTTP server supporting SSL.

- Replace fpem with the location of your .pem server file ('server.pem' by default).
- The default port is 5443.

Usage: python ulogme_serve_https.py


From https://www.piware.de/2011/01/creating-an-https-server-in-python/ and https://stackoverflow.com/a/22436756/5889533
"""
from __future__ import print_function   # Python 2 compatibility
from __future__ import absolute_import  # Python 2 compatibility

import os
import os.path
import webbrowser
import ssl
from subprocess import check_output
from http.server import HTTPServer, SimpleHTTPRequestHandler


# Utility functions

def generate_certificate(fpem="server.pem"):
    print("Generating the SSL certificate to {} in the current directory ({}) ...".format(fpem, os.getcwd()))
    args = [
        "openssl",
        "req",
        "-newkey rsa:4096",
        "-x509",
        "-keyout server.pem",
        "-out server.pem",
        "-days 365",  # Only valid one year!
        "-nodes"
    ]
    print("Executing '{}' ...".format(' '.join(args)))
    print(check_output(' '.join(args), shell=True))


def open_tab(url="https://localhost:5443/"):
    print("Opening the page '{}' in your favorite web browser ...".format(url))
    return webbrowser.open(url)


def test():
    """ Simple test. """
    # Parameters
    server_address = ("localhost", 5443)  # (address, port)
    # FIXME back to 443 ?
    print("Asking to use the address {s[0]} and the port {s[1]} ...".format(s=server_address))
    fpem = "server.pem"
    if not os.path.isfile(fpem):
        generate_certificate(fpem)
    print("Using the SSL certificate from the information in the file {} ...".format(fpem))

    # Starting...
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    httpd.socket = ssl.wrap_socket(httpd.socket, certfile=fpem, server_side=True)
    sa = httpd.socket.getsockname()
    print("Serving HTTPS on {} and port {} ...".format(sa[0], sa[1]))
    # Open the page...
    # open_tab("http://{}:{}/".format(sa[0], sa[1]))
    open_tab("https://{}:{}/".format(sa[0], sa[1]))
    # Start...
    try:
        httpd.serve_forever()
    finally:
        if httpd is not None:
            print("\nClosing the HTTPS server (address '{}', port '{}') ...".format(sa[0], sa[1]))
            httpd.server_close()


if __name__ == "__main__":
    test()
