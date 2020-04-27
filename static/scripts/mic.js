const getUserMedia = require('get-user-media-promise');
const MicrophoneStream = require('microphone-stream');
const ss = require('socket.io-stream');
const fs = require("fs");

const Pitchfinder = require("pitchfinder");
const detectPitch = Pitchfinder.YIN();
  // const io = require('socket.io-client');

var stream = ss.createStream();

const fps = 24
var startTime = new Date()

const average = arr => arr.reduce((sume, el) => sume + el, 0) / arr.length;

waveData = []

$(document).ready( () =>{

  $("#start").click(()=>{
    startTime = new Date();
    socket.emit("clickyclicky");

    alert("button got clicky clicky :3")
    // note: for iOS Safari, the constructor must be called in response to a tap, or else the AudioContext will remain
    // suspended and will not provide any audio data.
    var micStream = new MicrophoneStream({
        // stream: null,
        // objectMode: false,
        bufferSize: 256,
        // context: null
      });

    // ss(socket).emit('audStream', stream);


   
    getUserMedia({ video: false, audio: true })
      .then(function(strm) {
        micStream.setStream(strm);
      }).catch(function(error) {
        console.log(error);
      });
   
    // get Buffers (Essentially a Uint8Array DataView of the same Float32 values)
    micStream.on('data', function(chunk) {


      if((new Date() - startTime) > (1000/fps)){
        startTime = new Date()
        // Optionally convert the Buffer back into a Float32Array
        // (This actually just creates a new DataView - the underlying audio data is not copied or modified.)
        var raw = MicrophoneStream.toRaw(chunk)
        socket.emit("sendAud",raw);        
      }

      // stream.write(raw);
      // stream.pipe(fs.createWriteStream('temp.wav'))

      // const pitch = detectPitch(raw); // null if pitch cannot be i
      // console.log(pitch);
      

      // waveData.push(chunk)
   
      // note: if you set options.objectMode=true, the `data` event will output AudioBuffers instead of Buffers
     });
   
    // or pipe it to another stream
    // micStream.pipe(stream);
   
    // It also emits a format event with various details (frequency, channels, etc)
    micStream.on('format', function(format) {
      console.log(format);
    });
   
    // Stop when ready
    $("#stop").click(() => {
      micStream.stop();
      alert("owie!! X(");
      console.log("sending data chan to backend :3");
      socket.emit("getAudio",waveData);
      waveData = [];
    })



  })

})


