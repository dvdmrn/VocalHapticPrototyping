const fps = 30;

function drawSpectrum(samples,context,canvas) {
	context.clearRect(0,0,canvas[0].width,canvas[0].height);

	context.lineWidth = 2;
	for (i=0; i<samples.length; i++){
			context.beginPath();
			context.moveTo(0+(i*2), canvas[0].height);
			context.lineTo(0+(i*2), canvas[0].height - samples[i]*canvas[0].height);
			context.stroke();		
	}
}

$(document).ready(()=>{

	var c = $("#canvas");
	var ctx = c[0].getContext("2d");

	// 512 samples and canvas is 800 wide...


	socket.on("spectrum", (spec)=>{
		drawSpectrum(spec,ctx,c);
	})


})
