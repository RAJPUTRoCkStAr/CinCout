import streamlit as st
import streamlit.components.v1 as components

# Custom HTML and JavaScript for live camera feed
live_camera_feed = """
<!DOCTYPE html>
<html>
  <head>
    <style>
      video {
        width: 100%;
        height: auto;
      }
      #snapshot {
        display: none;
      }
    </style>
  </head>
  <body>
    <video id="video" autoplay></video>
    <button id="capture">Capture</button>
    <canvas id="snapshot"></canvas>
    <script>
      (function() {
        var video = document.getElementById('video');
        var canvas = document.getElementById('snapshot');
        var captureButton = document.getElementById('capture');
        var context = canvas.getContext('2d');
        var stream;
        navigator.mediaDevices.getUserMedia({ video: true })
          .then(function(s) {
            stream = s;
            video.srcObject = stream;
          })
          .catch(function(err) {
            console.error("Error: " + err);
          });

        captureButton.addEventListener('click', function() {
          context.drawImage(video, 0, 0, canvas.width, canvas.height);
          var dataUrl = canvas.toDataURL('image/png');
          fetch('http://localhost:8501/', {
            method: 'POST',
            body: JSON.stringify({ image: dataUrl }),
            headers: { 'Content-Type': 'application/json' }
          });
        });
      })();
    </script>
  </body>
</html>
"""

# Display the live camera feed in Streamlit
components.html(live_camera_feed, height=500)

# Streamlit code to handle the received image
if st.button('Refresh'):
    image_data = st.experimental_get_query_params().get('image', None)
    if image_data:
        st.image(image_data, caption='Captured Image')
