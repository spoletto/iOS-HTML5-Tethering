/* 
 * Server-side websocket server.
 *
 */

var ws = require("websocket-server");

var server = ws.createServer();

// Add a listener for new websocket connections.
server.addListener("connection", function(connection) {
	console.log("Websocket connection established.")
	connection.addListener("message", function(msg) {
		console.log("recevied message " + msg);
	});
});

server.listen(8080);