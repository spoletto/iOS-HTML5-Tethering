iOS-HTML5-Tethering
===============

iOS-HTML5-Tethering is a simple attempt to provide connectivity to a laptop in need of internet via a websocket-enabled smartphone browser. The project consists of three parts:

1. A websocket server running on the computer in need of internet, which establishes a connection between the laptop and the smartphone device. The laptop is configured to redirect all of its network traffic over the websocket connection, so that IP packets are sent to the smartphone device.
2. A websocket server running on a remote server, accessible by public IP. The remote server serves as a NAT, by reading all received IP packets and sending them out to the open internet as though the machine itself initiated the requests.
3. An HTML5 web app, which enables communication between the client and server machines by piping data between two websocket connections.

The websocket servers on both the client and remote end have been implemented using Node.js, though the implementation could easily be re-written using a number of other libraries/languages.

This project was created for the sole purpose of learning and experimenting with network technologies. This code should not be used in any production environments.

Client Setup - Mac OS X
------------------------

In order for all network traffic to be funneled through the websocket connection, a tun interface must be created on the client machine. If you haven't already, download and install the [TunTap package for Mac OS X](http://tuntaposx.sourceforge.net/download.xhtml). Once the TunTap package has been installed, create an ad-hoc network on the client machine:

1. Click on the AirPort icon in your menu bar. From the AirPort menu, select "Create Network..."
2. Provide a name for the network, and optionally provide a password.

When the HTML5 web app is loaded on your smartphone device, it will attempt to connect to a known, fixed IP address: `169.254.134.89`. Before we can run the websocket server which will bind to that address, we must assign that IP address to the Wifi device of the client machine. To do so, run the following command, substituting `en1` with your Wifi device name.

``` bash
$ sudo /sbin/ifconfig en1 inet 169.254.134.89 netmask 255.255.0.0 alias
```

Now, we can launch the websocket server.

``` bash
$ sudo node client/ws-server.js 
```

The websocket server will bind to `169.254.134.89:6354` and listen for new websocket connections.

Then, the websocket server will bring up a tun interface named `tun0` and assign the IP address `10.0.0.1` to it.

``` bash
$ sudo ifconfig tun0 10.0.0.1 10.0.0.1 netmask 255.255.255.0 up
```

It will then modify the IP routing table on the host machine to funnel all network traffic through the `tun0` device.

``` bash
$ sudo route delete default
$ sudo route add default 10.0.0.1
```

Now as network requests are issued, data will be written into `/dev/tun0`. The Node.js program will read all such data and broadcast it to connected clients. Similarly, as websocket messages are received, the Node.js program will write data into `/dev/tun0`, effectively injecting websocket data into the OS as received IP traffic.

Server Setup
------------

The server implementation was tested with an Amazon EC2 Micro Instance running Ubuntu Server Cloud Guest 11.10 (Oneiric Ocelot). A bootstrap script, `server/bootstrap_server.sh` is provided to install the necessary tools to get off the ground.


