iOS-HTML5-Tethering
===============

iOS-HTML5-Tethering is a simple attempt to provide connectivity to a laptop in need of internet via a websocket-enabled smartphone browser. The project consists of three parts:

1. A websocket server running on the computer in need of internet, which establishes a connection between the laptop and the smartphone device. The laptop is configured to redirect all of its network traffic over the websocket connection, so that IP packets are sent to the smartphone device.
2. A websocket server running on a remote server, to which the smartphone device also establishes a connection. The remote server serves as a NAT, by reading all received IP packets and sending them out to the open internet as though the machine itself initiated the requests.
3. An HTML5 web app, which enables communication between the client and server machines by piping data between two websocket connections.