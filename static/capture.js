(function() {
  // The width and height of the captured photo. We will set the
  // width to the value defined here, but the height will be
  // calculated based on the aspect ratio of the input stream.

  var width = 320;    // We will scale the photo width to this
  var height = 0;     // This will be computed based on the input stream

  // |streaming| indicates whether or not we're currently streaming
  // video from the camera. Obviously, we start at false.

  var streaming = false;

  // The various HTML elements we need to configure or control. These
  // will be set by the startup() function.

  var video = null;
  var canvas = null;
  var photo = null;
  var startbutton = null;
  var timer = null;
  function startup() {
    video = document.getElementById('video');
    canvas = document.getElementById('canvas');
    photo = document.getElementById('photo');
    startbutton = document.getElementById('startbutton');
	timer = document.getElementById('timer');
    navigator.mediaDevices.getUserMedia({video: true, audio: false})
    .then(function(stream) {
      video.srcObject = stream;
      video.play();
    })
    .catch(function(err) {
      console.log("An error occurred: " + err);
    });

    video.addEventListener('canplay', function(ev){
      if (!streaming) {
        height = video.videoHeight / (video.videoWidth/width);
      
        // Firefox currently has a bug where the height can't be read from
        // the video, so we will make assumptions if this happens.
      
        if (isNaN(height)) {
          height = width / (4/3);
        }
      
        video.setAttribute('width', width);
        video.setAttribute('height', height);
        canvas.setAttribute('width', width);
        canvas.setAttribute('height', height);
        streaming = true;
      }
    }, false);

    startbutton.addEventListener('click', function(ev){
      //countdown2();
	  takepicture();
	  
      ev.preventDefault();
    }, false);
    
    clearphoto();
  }

  // Fill the photo with an indication that none has been
  // captured.

  function clearphoto() {
    var context = canvas.getContext('2d');
    context.fillStyle = "#AAA";
    context.fillRect(0, 0, canvas.width, canvas.height);

    var data = canvas.toDataURL('image/png');
    photo.setAttribute('src', data);
  }
  
  function countdown2(){
  var i=0, j=5;
var iv = setInterval(function() {
    timer.innerHTML = toString(i) + "so ";
	console.log(i);
	//var start = new Date().getTime();
	//while(true){
	//var now = new Date().getTime();
	//var distance = now-start;
	//var passedSec = Math.floor((distance % (1000 * 60)) / 1000);
	//if(passedSec >= 1){break};
    // things that take a while to do
    if (++i>=j) clearInterval(iv);
}, 1000);

  }
  
  function countdown(){

		// Get today's date and time
		var start = new Date().getTime();
		var seconds = 5
		// Find the distance between now and the count down date
		while(true){
			var now = new Date().getTime();
			var distance = now-start;
		
			// Time calculations for days, hours, minutes and seconds
			passedSec = Math.floor((distance % (1000 * 60)) / 1000);
			
			if(passedSec > 1){
				start = new Date().getTime();
				// Output the result in an element with id="demo"
				// document.getElementById("timer").innerHTML = toString(seconds) + "s ";
				timer.innerHTML = 'hsoef' + "sajefajfepoaijfeposiajpfeoijapweofijaepwoij ";
				console.log(timer.innerHTML)
				seconds = seconds - 1
				console.log(seconds)
			}
		
		// If the count down is over, write some text 
		if (seconds < 0) {
			// document.getElementById("timer").innerHTML = "0";
			timer.innerHTML = toString(seconds) + "s ";
			return
		}
  }
}
  
  function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}
  
  // Capture a photo by fetching the current contents of the video
  // and drawing it into a canvas, then converting that to a PNG
  // format data URL. By drawing it on an offscreen canvas and then
  // drawing that to the screen, we can change its size and/or apply
  // other changes before drawing it.

  async function takepicture() {
    var context = canvas.getContext('2d');
	//countdown()
	document.getElementById("timer").innerHTML = "5";
	await sleep(1000)
	document.getElementById("timer").innerHTML = "4";
	await sleep(1000)
	document.getElementById("timer").innerHTML = "3";
	await sleep(1000)
	document.getElementById("timer").innerHTML = "4";
	await sleep(1000)
	document.getElementById("timer").innerHTML = "2";
	await sleep(1000)
	document.getElementById("timer").innerHTML = "1";
	await sleep(1000)
	document.getElementById("timer").innerHTML = "0";
	await sleep(1000)
    if (width && height) {
      canvas.width = width;
      canvas.height = height;
      context.drawImage(video, 0, 0, width, height);
    
      var data = canvas.toDataURL('image/png');
      photo.setAttribute('src', data);
	  var formData = new FormData();
	  formData.append('sendID',sendID);
	  formData.append('img',data);
	  var request = new XMLHttpRequest();
	  request.open('POST', '/'+sendID);
	  request.send(formData);

    } else {
		
      clearphoto();
    }
	
  }

  // Set up our event listener to run the startup process
  // once loading is complete.
  window.addEventListener('load', startup, false);
})();