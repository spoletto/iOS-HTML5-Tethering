#!/usr/bin/env python

from tornado.websocket import WebSocketHandler
from tornado.httpserver import HTTPServer
from tornado.web import Application
from tornado.ioloop import IOLoop

import subprocess
import threading
import os

# Initialize the tun0 device.
tun = os.open('/dev/tun0', os.O_RDWR)

# Assign a fixed, known alias address to the wifi card.
subprocess.check_call('sudo /sbin/ifconfig en1 inet 169.254.134.89 netmask 255.255.0.0 alias', shell=True)

# Bring up the tun device and assign the IP address 10.0.0.1 to it.
subprocess.check_call('sudo ifconfig tun0 10.0.0.1 10.0.0.1 netmask 255.255.255.0 up', shell=True)

# Modify the IP routing table on the host machine to funnel all network traffic through tun0.
subprocess.check_call('sudo route delete default', shell=True)
subprocess.check_call('sudo route add default 10.0.0.1', shell=True)

# Currently only capable of managing a single websocket connection.
# Not thread-safe.
connection = None

class TunReader(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self) 

    def run(self):
        global connection
        global tun
        while (True):
            dataFromTun = os.read(tun, 1500).encode('base64')  
            if connection:
                connection.write_message(dataFromTun)

class Handler(WebSocketHandler):
        def open(self):
            global connection
            print "New connection opened."
            connection = self

        def on_message(self, message):
            global tun
            print "raw message: " + message
            m = message.decode('base64')
            print "message received from websocket: " + m
            os.write(tun, m)

        def on_close(self):
            global connection
            print "Connection closed."
            connection = None

        def allow_draft76(self):
            return True

tunThread = TunReader()
tunThread.daemon = True
tunThread.start()

wsServer = HTTPServer(Application([("/websocket", Handler)]))
print "Server started."
wsServer.listen(6354, "169.254.134.89")
IOLoop.instance().start()