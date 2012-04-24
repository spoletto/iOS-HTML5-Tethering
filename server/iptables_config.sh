#!/bin/bash

# Before executing Scapy scripts, it is necessary to disable 
# the linux kernel’s own responses. If the linux kernel is allowed 
# to answer arriving network packets, it will answer with RST 
# during the TCP handshake, because the kernel believes that 
# no port is open. For TCP, disable the kernel’s response with:
sudo iptables -A OUTPUT -p tcp --tcp-flags RST RST -j DROP
