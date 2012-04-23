#!/usr/bin/env python

from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.web import Application
from tornado.websocket import WebSocketHandler
import threading
import subprocess

tun = open('/dev/tun0', 'r+')

subprocess.check_call('sudo ifconfig tun0 10.0.0.1 10.0.0.1 netmask 255.255.255.0 up', shell=True)
subprocess.check_call('sudo route delete default', shell=True)
subprocess.check_call('sudo route add default 10.0.0.1', shell=True)

connection = None

class TunReader(threading.Thread):
    def __init__(self, server):
        self.server = server
        threading.Thread.__init__(self) 

    def run(self):
        print "Tunnel listening thread started."
        while (True):
            dataFromTun = tun.read()
            #dataFromTun = dataFromTun.decode('bin')       
            print "message received from tunnel: " + dataFromTun
            if connection:
                connection.write_message(dataFromTun)

class Handler(WebSocketHandler):
        def open(self):
            print "New connection opened."
            connection = self

        def on_message(self, message):
            print "raw message: " + message
            m = message.decode('ascii').encode('utf-8')
            print "message received from websocket: " + m
            tun.write(m)

        def on_close(self):
            print "Connection closed."
            connection = None

        def allow_draft76(self):
            return True


wsServer = HTTPServer(Application([("/websocket", Handler)]))
tunThread = TunReader(wsServer)
tunThread.start()
print "Server started."
wsServer.listen(6354, "169.254.134.89")
IOLoop.instance().start()