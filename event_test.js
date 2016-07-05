var events = require("events");
var eventEmitter = new events.EventEmitter();

var conHandler = function connected(){
    console.log("connection successful!");
    eventEmitter.emit('data_received');
}

eventEmitter.on('connection', conHandler);

var data_receive = function recv(){
    console.log("recv...");

}

eventEmitter.emit('connection');


console.log("OK");
