const express = require('express');
const app = express();
const path = require('path');
const bodyParser = require('body-parser');

var server = require('http').createServer(app);  
var sio = require('socket.io')(server,{transports: ['websocket']});

// parse application/x-www-form-urlencoded
app.use(bodyParser.urlencoded({ extended: false }))
// parse application/json
app.use(bodyParser.json())
// parse various different custom JSON types as JSON
app.use(bodyParser.json({ type: 'application/*+json' }))
// parse some custom thing into a Buffer
app.use(bodyParser.raw({ type: 'application/vnd.custom-type' }))
// parse an HTML body into a string
app.use(bodyParser.text({ type: 'text/html' }))

app.get('/', function(req, res) {
    res.sendFile(path.join(__dirname + '/index.html'));
});

let getprogress = "0%";
let done = false;

function getTime() {
    let d = new Date();
    return d.getHours() + ":" + d.getMinutes() + ":" + d.getSeconds()
}

app.post('*', function(req, res) {
    console.log(req.body);
    if (undefined != req.body.init){
        sio.emit("commandMessage",{command:"initialize",data:{}})
        res.send(getTime() + " - sending initialize!");
    }
    else if (undefined != req.body.start){
        sio.emit("commandMessage",{command:"start",data:{}})
        res.send(getTime() + " - sending start!");
    }
    else if (undefined != req.body.stop){
        sio.emit("commandMessage",{command:"stop",data:{}})
        res.send(getTime() + " - sending stop!");
    }
    else if (undefined != req.body.getprogress){
        res.send(getTime() + " - progress is : "+ getprogress);
    }
    else if (undefined != req.body.refreshprogress){
        sio.emit("commandMessage",{command:"progress",data:{}})
        res.send(getTime() + " - sending state refresh request. to see recent state press 'get state' button");
    }
});


sio.on('connection', function(client) {  
    console.log('Client connected...');

    client.on('disconnect', function(data) {
        console.log('Client disconnected...');
    });
    client.on('reconnect', function(data) {
        console.log('Client disconnected...');
    });

     client.on('commandMessage', function(data) {
         if (data!=undefined){
    //         progress = data[].progress;
         console.log(data);
        }
     });
});


app.listen(3000);
























// var express = require('express');
// var app = express();
// var http = require('http');
// var server = http.createServer(app);
// const socketio = require('socket.io');

// //app.use(express.bodyParser());
// app.post('/', function(req, res) {
//   console.log(req.body);
//   res.send(200);

// });

// app.get('/', function(req, res) {
//     console.log(req.body);
//     res.send(200);
    
// });

// const port = 3333;

// // //server.listen(process.env.PORT, process.env.IP);
// server.listen("127.0.0.1", port);
// // this._socketServer = socketio.listen(server);
// // this._socketServer.on('connection', (socket) => {
// //     log.info('Connected!!!')
// //     //this._registerSocketMessages(socket);
// //     this.emit('connection');
// // })