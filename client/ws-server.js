/* 
 * Before running the websocket server, 
 * address 169.254.134.89 must be available for binding.
 *
 * On Mac OS X, this is achieved by creating an ad-hoc network
 * via System Preferences, then running:
 * sudo /sbin/ifconfig en1 inet 169.254.134.89 netmask 255.255.0.0 alias
 *
 */

var exec = require('child_process').exec;
var ws = require("websocket-server");
var fs = require("fs");

var server = ws.createServer();
var fd = fs.openSync('/dev/tun0', 'r+');

// Add a listener for new websocket connections.
server.addListener("connection", function(connection) {
	console.log("Websocket connection established.")
	connection.addListener("message", function(msg) {
		// Write received websocket messages into the tunnel. 
		fs.write(fd, msg, 0, msg.length, null, function(err, written) {
			if (error !== null) {
				console.log('Write error: ' + error);
			}
		});
	});
});

// Continuously read from the tunnel and broadcast IP packets to all connected websockets.
var buffer = new Buffer(500);
function network_traffic_to_websocket() {
	fs.read(fd, buffer, 0, 500, 0, function(err, num) {
		server.broadcast(buffer.toString(0, num));
		network_traffic_to_websocket();
	});
}

// Bring up the tun0 device, assigning it the IP address 10.0.0.1.
exec("sudo ifconfig tun0 10.0.0.1 10.0.0.1 netmask 255.255.255.0 up", function (error, stdout, stderr) {
 	if (error !== null) { console.log('exec error: ' + error); }
	
	// Modify the IP routing table to delete the current default route, and route all network traffic through the tunnel.
	exec("sudo route delete default", function (error, stdout, stderr) {
		if (error !== null) { console.log('exec error: ' + error); }
		exec("sudo route add default 10.0.0.1", function (error, stdout, stderr) {
			if (error !== null) { console.log('exec error: ' + error); }
			network_traffic_to_websocket();
		});
	});
});

server.listen(6354, "169.254.134.89");