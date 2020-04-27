// imports =====================================================================

// express --
const express = require('express')
const app = express()
var http = require('http').createServer(app);

app.use(express.static('static'))
const port = process.env.PORT || 3000;
const server = app.listen(port, () => console.log(`Listening on port ${port}`))

// socket.io --
const io = require('socket.io')(server);
const ss = require('socket.io-stream');

var stream = ss.createStream();

// audio processing --
// const ap = require('audio-processing');
var ft = require('fourier-transform');
const Pitchfinder = require("pitchfinder");


const fs = require('fs');
var path = require('path');

// globals ---------------------------------------------------------------------
 
const detectPitch = Pitchfinder.AMDF();
var startTime = new Date()
const fps = 15

var k = 0

// functions ===================================================================

function makeSin(){
	var frequency = 440;
	var size = 1024;
	var sampleRate = 44100;
	var waveform = new Float32Array(size);
	for (var i = 0; i < size; i++) {
	    waveform[i] = Math.sin(frequency * Math.PI * 2 * (i / sampleRate));
	}
	
	return waveform
}

// wf = makeSin()
// //get normalized magnitudes for frequencies from 0 to 22050 with interval 44100/1024 ≈ 43Hz
// var spectrum = ft(wf);

function rms(vals){
	let mean_square = vals.map((x)=>x**2).reduce((a,b)=>a+b,0) / vals.length
	let rt = Math.sqrt(mean_square)
	return rt
}


function getVals(json){
	let values = Object.keys(json).map(function(key){
	    return json[key];
	});
	return values
}





// socket io events ============================================================

io.on('connection', (socket) => {

  console.log("io.on connection event!")

  socket.on("clickyclicky", ()=>{
  	startTime = new Date();
  	console.log("clickeeeddddd ;)");
  })

  socket.on("getAudio", (raw) => {
  	console.log("got data chan :3");
  	console.log(raw);
  })

  socket.on("newStimuli", () =>
  {
    io.emit("newStimuli");
  })

  // socket.on("getSpectrum", () =>
  // {
  // 	console.log("getting spectrum")
  // 	io.emit("spectrum",spectrum);
  // })

// .............................................................................
// main send aud event

  socket.on("sendAud", (data) =>{
  	let streamVals = getVals(data);
  	
  	// console.log("called! ",streamVals);
  	if((new Date()-startTime) > 1000/fps){
  		// new frame uwu
  		spec = ft(streamVals)
  	}
  	var amp = rms(streamVals);
  	io.emit("spectrum",spec);
  	var pitch = detectPitch(streamVals); // null if pitch cannot be i
  	console.log(pitch);


  })

  // stream events ---

  ss(socket).on("audStream", function(stream, data){

  	// let streamVals = getVals(data);

  	console.log("aud stream got!",stream);

  	// let filename = path.join(__dirname, 'temp.wav');
    // stream.pipe(fs.createWriteStream(filename));

  	// if((new Date()-startTime) > 1000/fps){
  	// 	// new frame uwu
  	// 	spec = ft(streamVals)
  	// }
  	// console.log(spec)
  	// io.emit("spectrum",spec);


  	// var filename = "temp.wav";
  	// stream.pipe(fs.createWriteStream(filename));
  })
})









// io.on('connection', (socket) => {
//   console.log('a user connected');
// });

// http.listen(3000, () => {
//   console.log('listening on *:3000');
// });





// const basicAuth = require('express-basic-auth')

// app.use(basicAuth({
//     users: { srl: 'eurohaptics' },
//     challenge: true // <--- needed to actually show the login dialog!
// }));



// const https = require('https')
// const fs = require('fs')


// app.get('/static/', (req, res) => {
//   res.send('WORKING!')
// })


// app.use(express.static('static'))
// const port = process.env.PORT || 3000;
// app.listen(port, () => console.log(`Listening on port ${port}`))


