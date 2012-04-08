iOS-HTML5-Tethering
===============

iOS-HTML5-Tethering is a simple attempt to provide connectivity to a laptop in need of internet via a websocket-enabled smartphone browser. The project consists of three parts:

1. A websocket server running on the computer in need of internet, which establishes a connection between the laptop and the smartphone device. The laptop is configured to redirect all of its network traffic over the websocket connection, so that IP packets are sent to the smartphone device.
2. A websocket server running on a remote server, accessible by public IP. The remote server serves as a NAT, by reading all received IP packets and sending them out to the open internet as though the machine itself initiated the requests.
3. An HTML5 web app, which enables communication between the client and server machines by piping data between two websocket connections.

This project was created for the sole purpose of learning and experimenting with network technologies. This code should not be used in any production environments.

Client Setup - Mac OS X
------------------------

In order for all network traffic to be funneled through the websocket connection, a tun interface must be created on the client machine.

1. Download the [TunTap package for Mac OS X](http://tuntaposx.sourceforge.net/download.xhtml).

Once the TunTap package has been installed, create an ad-hoc network on the client machine.

1. Click on the AirPort icon in your menu bar. From the AirPort menu, select "Create Network..."
2. Provide a name for the network, and optionally provide a password.

Now, on your smartphone device, join the ad-hoc network.

When the HTML5 web app is loaded on the device, it will attempt to connect to a known, fixed IP address: 169.254.134.89. Before we can run the websocket server which will bind to that address, we must assign that IP address to the Wifi device of the client machine:

1. Open terminal and run 'sudo /sbin/ifconfig en1 inet 169.254.134.89 netmask 255.255.0.0 alias'. Note: 'en1' may need to be substituted for a different device name.

Now, we can launch the websocket server.

1. sudo node client/ws-server.js 



