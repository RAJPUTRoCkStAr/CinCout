// Access the video element
const video = document.getElementById('video');

// Request camera access
if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
    navigator.mediaDevices.getUserMedia({ video: true }).then(function(stream) {
        // Set the video element's source to the camera stream
        video.srcObject = stream;
        video.play();
    }).catch(function(error) {
        console.error("Error accessing camera: ", error);
        document.getElementById('camera-placeholder').innerHTML = '<p>Camera access denied or not available.</p>';
    });
} else {
    console.error("getUserMedia not supported by this browser.");
    document.getElementById('camera-placeholder').innerHTML = '<p>Camera not supported by your browser.</p>';
}
