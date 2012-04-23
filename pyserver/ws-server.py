#!/usr/bin/env python

import threading
import codecs
import base64
import binascii

###### Tun device stuff ######

import fcntl
import os
import struct
import subprocess

TUNSETIFF = 0x400454ca
TUNSETOWNER = TUNSETIFF + 2
IFF_TUN = 0x0001
IFF_TAP = 0x0002
IFF_NO_PI = 0x1000

tun = open('/dev/net/tun', 'r+b')
ifr = struct.pack('16sH', 'tun0', IFF_TUN | IFF_NO_PI)
fcntl.ioctl(tun, TUNSETIFF, ifr)

#subprocess.check_call('ip tuntap add dev tun0 mode tun', shell=True)
#subprocess.check_call('ifconfig tun0 10.0.0.1', shell=True)

class TunReader(threading.Thread):
	def __init__(self, server):
		self.server = server
		threading.Thread.__init__(self)	

	def run(self):
		while (True):
			dataFromTun = tun.read()
			dataFromTun = dataFromTun.decode('utf-8')		
			print "message received from tunnel: " + dataFromTun
			self.server.write_message(dataFromTun)
			
###### Websocket stuff ########

from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.web import Application
from tornado.websocket import WebSocketHandler

class Handler(WebSocketHandler):
        def open(self):
            print "New connection opened."

        def on_message(self, message):
		print "raw message: " + message
		m = message.decode('ascii').encode('utf-8')
                print "message received from websocket: " + m
		#tun.write(m)

        def on_close(self):
                print "Connection closed."

        def allow_draft76(self):
                return True

wsServer = HTTPServer(Application([("/websocket/", Handler)]))

tunThread = TunReader(wsServer)
tunThread.start()

print "Server started."
wsServer.listen(8080)
IOLoop.instance().start()

