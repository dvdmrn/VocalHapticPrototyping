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
var ft = require('fourier-transform');
const Pitchfinder = require("pitchfinder");
const wavefile = require('wavefile');

const fs = require('fs');
var path = require('path');

// globals ---------------------------------------------------------------------
 
const detectPitch = Pitchfinder.AMDF();
var startTime = new Date()
const fps = 60

var recStartTime = new Date()
var recStopTime = new Date()

var k = 0

var amp_vals = []
var pitch_vals = []
var fricative_vals = []
var sibilant_vals = []

var wav = new wavefile.WaveFile();



const gain = 5;

// functions ===================================================================

 
// Create a mono wave file, 44.1 kHz, 32-bit and 4 samples

function makeWavFile(sampleArray,path){
  
  // 16 bit signed int range is 32,768
  wav.fromScratch(1, 44100, '16', sampleArray);
  fs.writeFileSync(path, wav.toBuffer());
  console.log("wrote to: ",path,"!")

}

function scaleSineWaveInt16(sin){
  return sin.map((x)=>Math.floor(x*3276));
}


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

function scaleRange(num, in_min, in_max, out_min, out_max){
  return (num - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}

// wf = makeSin()
// //get normalized magnitudes for frequencies from 0 to 22050 with interval 44100/1024 ≈ 43Hz
// var spectrum = ft(wf);

function meanSquare(vals){
  let mean_square = vals.map((x)=>x**2).reduce((a,b)=>a+b,0) / vals.length
  return mean_square
}
function rms(vals){
	let mean_square = meanSquare(vals);
	let rt = Math.sqrt(mean_square)
	return rt
}

function detectSibilant(spectrum){
  let cutoff = 5;
  let left = spectrum.slice(0,cutoff)
  let right = spectrum.slice(cutoff,spectrum.length)
  let ms_l = meanSquare(left);
  let ms_r = meanSquare(right);

  if (ms_r > ms_l){
    return 1
  }
  else{
    return 0
  }

}

function getVals(json){
	let values = Object.keys(json).map(function(key){
	    return json[key];
	});
	return values
}

function scalePitchVals(pitch_array){
  let scaledPitch = []
  for (var i = 0; i < pitch_array.length; i++) {
    if(pitch_array[i] === null){
      scaledPitch.push(1)
    }
    else{
      let scaled = scaleRange(pitch_array[i],170, 300,1,7);
      scaledPitch.push(scaled);
    }
  }
  console.log("prev pitch: ")
  console.log(pitch_array)
  console.log("scaled pitch: ")
  console.dir(scaledPitch, {'maxArrayLength': null});
  // console.log(scaledPitch)
  return scaledPitch;
}

function makeVibration(){
  console.log("creating vibrotactile signal");

  let frequency = 50; // modify with pitch
  let sampleRate = 44100;


  let recTime = recStopTime - recStartTime;
  let n_amps = amp_vals.length;
  let n_pitch = pitch_vals.length;

  let pitchModifer = scalePitchVals(pitch_vals);
  let wf_length = Math.floor((recTime/1000)*sampleRate);
  let waveform = new Float32Array(wf_length);

  let keyVal_spacing_ms = (recTime/n_amps) // ms apart between key values
  let keyVal_spacing_samples = Math.floor((keyVal_spacing_ms / 1000)*sampleRate);

  // console.log("should be writing this many amp terms: ",n_amps," width: ",keyVal_spacing_samples);
  console.log("length:",recTime)
  // construct sine --
  k = 0;
  for (var i = 0; i < wf_length; i++) {

      waveform[i] = Math.sin(pitchModifer[k] * frequency * Math.PI * 2 * (i / sampleRate))*(amp_vals[k]*10);
      if ((i%keyVal_spacing_samples) == 0){
        k++
        // console.log("wrote amp term ",k," @ sample: ",i)
      }
  }



  Int16Sine = scaleSineWaveInt16(waveform);
  makeWavFile(Int16Sine, "temp.wav");
   
}


// socket io events ============================================================

io.on('connection', (socket) => {

  console.log("io.on connection event!")

  socket.on("clickyclicky", ()=>{
  	startTime = new Date();
    recStartTime = new Date();
    amp_vals = []
    pitch_vals = []
    fricative_vals = []
  	console.log("clickeeeddddd ;)");
  })

  socket.on("stop", () => {
  	console.log("stopping");
    recStopTime = new Date();
    makeVibration();
  	
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
  	let amp = rms(streamVals);
    sibilantVals.push(detectSibilant(spec))
  	io.emit("spectrum",spec);
  	var pitch = detectPitch(streamVals); // null if pitch cannot be i
  	// console.log(pitch);

    amp_vals.push(amp);
    pitch_vals.push(pitch);


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


