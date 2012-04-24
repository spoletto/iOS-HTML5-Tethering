#!/usr/bin/env python

from tornado.websocket import WebSocketHandler
from tornado.httpserver import HTTPServer
from tornado.web import Application
from tornado.ioloop import IOLoop

from collections import defaultdict
from scapy.all import *
import threading

# Warning: Not thread-safe.
# Dictionary mapping (outbound.dst, outbound.dport) -> count of IP packets awaiting reply
outbound_packets = defaultdict(int)
connection = None

class PacketSniffer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self) 

    def run(self):
        global connection
        while (True):
            pkt = sniff(iface="eth0", count=1)
            if not pkt[0].haslayer(IP) or not pkt[0].haslayer(TCP):
                continue # Just handle TCP for now.
            pkt = pkt[0][IP]
            
            if outbound_packets[(pkt.src, pkt.sport)] > 0:
                outbound_packets[(pkt.src, pkt.sport)] -= 1
                
                # Modify the destination address back to the address of the TUN on the host.        
                pkt.dst = "10.0.0.1"
                del pkt[TCP].chksum
                del pkt[IP].chksum
                pkt.show2() # Force recompute the checksum
    
                if connection:
                    connection.write_message(str(pkt).encode('base64'))
            

class Handler(WebSocketHandler):
    def open(self):
        global connection
        print "New connection opened."
        connection = self

    def manipulate_outgoing_packet(self, message):
        # Add the original packet to the NAT table.
        global outbound_packets
        ipPacket = IP(message)
        outbound_packets[(ipPacket.dst, ipPacket.dport)] += 1
        
        # Modify the source IP address and recalculate the checksum.
        ipPacket.src = "10.202.43.31"
        del ipPacket[TCP].chksum
        del ipPacket[IP].chksum
        send(ipPacket)
        
    def on_message(self, message):
        self.manipulate_outgoing_packet(message.decode('base64'))

    def on_close(self):
        global connection
        print "Connection closed."
        connection = None

    def allow_draft76(self):
        return True

sniffingThread = PacketSniffer()
sniffingThread.daemon = True
sniffingThread.start()
            
wsServer = HTTPServer(Application([("/websocket/", Handler)]))
print "Server started."
wsServer.listen(8080)
IOLoop.instance().start()