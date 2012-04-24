iOS-HTML5-Tethering
===============

iOS-HTML5-Tethering is a simple attempt to provide connectivity to a laptop in need of internet via a websocket-enabled smartphone browser. The project consists of three parts:

1. A websocket server running on the computer in need of internet, which establishes a connection between the laptop and the smartphone device. The laptop is configured to redirect all of its network traffic over the websocket connection, so that IP packets are sent to the smartphone device.
2. A websocket server running on a remote server, accessible by public IP. The remote server serves as a NAT, by reading all received IP packets and sending them out to the open internet as though the machine itself initiated the requests.
3. An HTML5 web app, which enables communication between the client and server machines by piping data between two websocket connections.

The websocket servers on both the client and remote end have been implemented using Twisted, though the implementation could easily be re-written using a number of other libraries/languages.

This project was created for the sole purpose of learning and experimenting with network technologies. This code should not be used in any production environments.

Client Setup - Mac OS X
------------------------

In order for all network traffic to be funneled through the websocket connection, a tun interface must be created on the client machine. If you haven't already, download and install the [TunTap package for Mac OS X](http://tuntaposx.sourceforge.net/download.xhtml). Once the TunTap package has been installed, create an ad-hoc network on the client machine:

1. Click on the AirPort icon in your menu bar. From the AirPort menu, select "Create Network..."
2. Provide a name for the network, and optionally provide a password.

Now run the client-side websocket server:

``` bash
$ sudo python client/client-ws-server.py 
```

The client-side websocket server will:

1. Initialize a tun0 virtual device.
2. Assign a fixed, known alias address (`169.254.134.89`) to the Wifi card.
3. Bring up the tun device and assign the IP address 10.0.0.1 to it.
4. Modify the IP routing table on the host machine to funnel all network traffic through tun0.
5. Bind to `169.254.134.89:6354` and listen for new websocket connections.
6. Spawn a thread to continuously read from tun0 and forward received data to the connected websocket client.


Server Setup
------------

The server implementation was tested with an Amazon EC2 Micro Instance running Ubuntu Server Cloud Guest 11.10 (Oneiric Ocelot). A bootstrap script, `server/bootstrap_server.sh` is provided to install the necessary tools to get off the ground. Once the bootstrap script has completed, run both the static file server and the websocket server:

``` bash
$ sudo node server/fs-server.js
$ sudo python server/ws-server.py
```

The static file server will serve the HTML5 web app when the public URL of the EC2 instance is requested.

The websocket server will:

1. Bind to port 8080 and listen for new websocket connections.
2. Construct IP packets using received websocket messages and modify the source IP address before sending it out via eth0.
3. Sniff incoming packets on eth0 and look for IP packets that look like responses to outgoing requests. These responses will be written back to the websocket, thereby communicating the response back to the client in need of internet.

Limitations
------------

- Neither the remote server nor the client websocket server handle more than one websocket connection at a time
- While theoretically the architecture presented here could be used to tether any IP traffic, the current implementation only handles TCP packets.
- If DNS is not configured on the client machine, hostnames will not be resolved.
