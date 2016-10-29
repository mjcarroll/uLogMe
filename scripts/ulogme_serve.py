#!/usr/bin/env python2
# -*- coding: utf8 -*-
# ulogme_serve.py for https://github.com/Naereen/uLogMe/
# MIT Licensed, https://lbesson.mit-license.org/
#
from __future__ import print_function   # Python 2 compatibility
from __future__ import absolute_import  # Python 2 compatibility

import sys
import os
import SocketServer
import SimpleHTTPServer
import cgi
import subprocess
import socket

# Local imports
from export_events import updateEvents
from rewind7am import rewindTime
from notify import notify


# Import a printc function to use ANSI colors in the stdout output
try:
    try:
        from ansicolortags import printc
    except ImportError:
        print("Optional dependancy (ansicolortags) is not available, using regular print function.")
        print("  You can install it with : 'pip install ansicolortags' (or sudo pip)...")
        from ANSIColors import printc
except ImportError:
    print("Optional dependancy (ANSIColors) is not available, using regular print function.")
    print("  You can install it with : 'pip install ANSIColors-balises' (or sudo pip)...")

    def printc(*a, **kw):
        """ Fake function printc.

        ansicolortags or ANSIColors are not installed...
        Install ansicolortags from pypi (with 'pip install ansicolortags')
        """
        print(*a, **kw)


# Convenience functions

def writenote(note, time_=None):
    """ From https://github.com/karpathy/ulogme/issues/48"""
    cmd = ["../scripts/note.sh"]
    if time_ is not None:
        cmd.append(str(time_))
    process = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    process.communicate(input=note)
    process.wait()
    notify("uLogMe created a note, with content '{}' and time '{!s}'.".format(note, time_), "uLogMe : note")
    printc("<green>uLogMe created a note<white>, with content '<black>{}<white>' and time '<magenta>{!s}<white>'.".format(note, time_))


# Custom handler
class CustomHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_GET(self):
        # default behavior
        SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={
                "REQUEST_METHOD": "POST",
                "CONTENT_TYPE": self.headers["Content-Type"]
            }
        )
        result = "NOT_UNDERSTOOD"

        if self.path == "/refresh":
            printc("<green>Refreshing the view of uLogMe ...<white>")
            notify("Refreshing the view of uLogMe ...")
            # Recompute jsons. We have to pop out to root from render directory
            # temporarily. It's a little ugly
            refresh_time = form.getvalue("time")
            os.chdir(rootdir)  # pop out
            updateEvents()  # defined in export_events.py
            os.chdir(os.path.join("..", "render"))  # pop back to render directory
            result = "OK"

        if self.path == "/addnote":
            printc("<green>Adding a note in uLogMe ...<white>")
            notify("Adding a note in uLogMe ...", icon="note")
            # add note at specified time and refresh
            note = form.getvalue("note")
            note_time = form.getvalue("time")
            os.chdir(rootdir)  # pop out
            writenote(note, note_time)
            updateEvents()  # defined in export_events.py
            os.chdir(os.path.join("..", "render"))  # go back to render
            result = "OK"

        if self.path == "/blog":
            printc("<green>Adding a blog post in uLogMe ...<white>")
            notify("Adding a blog post in uLogMe ...", icon="note")  # DEBUG
            # add note at specified time and refresh
            post = form.getvalue("post")
            if post is None:
                post = ""
            post_time = int(form.getvalue("time"))
            os.chdir(rootdir)  # pop out
            trev = rewindTime(post_time)
            with open(os.path.join("..", "logs", "blog_%d.txt" % (post_time, )), "w") as f:
                f.write(post)
            updateEvents()  # defined in export_events.py
            os.chdir(os.path.join("..", "render"))  # go back to render
            result = "OK"

        # This part has to be done manually
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(result)


if __name__ == "__main__":
    httpd = None  # Make sure the variable exist, or the finally: case below can mess up

    # Port settings
    if len(sys.argv) > 1:
        PORT = int(sys.argv[1])
        assert PORT > 2024, "Error, you should not ask to use a PORT reserved by the system (<= 2024)"
    else:
        PORT = 8124

    # Address settings
    if len(sys.argv) > 2:
        IP = str(sys.argv[2])
    else:
        IP = "127.0.0.1"  # IP address to use by default
        # Instead of "", thanks to https://github.com/karpathy/ulogme/issues/48

    # serve render/ folder, not current folder
    rootdir = os.getcwd()
    os.chdir(os.path.join("..", "render"))

    try:
        httpd = SocketServer.ThreadingTCPServer((IP, PORT), CustomHandler)
        printc("<green>Serving uLogMe<white> on a HTTP server, see it locally on '<black>http://{}:{}<white>' ...".format(IP, PORT))
        notify("Serving uLogMe on a HTTP server, see it locally on 'http://{}:{}' ...".format(IP, PORT), icon="terminal")  # DEBUG
        httpd.serve_forever()
    except socket.error as e:
        if e.errno == 98:
            printc("<red>The port {} was already used ...<white>".format(PORT))
            printc("Try again in some time (about 1 minute on Ubuntu), or launch the script again with another port: '<black>$ ulogme_serve.py {}<white>' ...".format(PORT + 1))
        else:
            printc("<red>Error, ulogme_serve.py was interrupted, giving:<white>")
            printc("<red>Exception:<white> e =", e)
            # print("Exception: dir(e) =", dir(e))  # DEBUG
    except KeyboardInterrupt:
        printc("\n<red>You probably asked to interrupt<white> the '<black>ulogme_serve.py<white>' HTTP server ...")
    finally:
        try:
            if httpd is not None:
                printc("\n<yellow>Closing the HTTP server<white> (address '<black>{}<white>', port '<black>{}<white>') ...".format(IP, PORT))
                httpd.server_close()
        except Exception as e:
            printc("<red>The HTTP server<white> (address '<black>{}<white>', port '<black>{}<white>') <red>might not have been closed<white> ...".format(IP, PORT))
            printc("<red>Exception:<white> e =", e)
