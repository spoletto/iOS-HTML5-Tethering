/* 
 * Server-side websocket server.
 *
 */

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

server.listen(8080);