import streamlit as st
from gtts import gTTS
from io import BytesIO
import base64

# Function to convert text to speech
def speak(text):
    tts = gTTS(text=text, lang='en')
    audio_fp = BytesIO()  # Create a file-like object in memory
    tts.write_to_fp(audio_fp)
    audio_fp.seek(0)  # Go back to the start of the audio file
    
    # Encode audio file in base64 to inject into HTML
    audio_base64 = base64.b64encode(audio_fp.read()).decode()
    audio_html = f"""
        <audio autoplay="true">
            <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
        </audio>
    """
    # Inject JavaScript/HTML to play the audio automatically
    st.markdown(audio_html, unsafe_allow_html=True)

# Streamlit app
st.title("Auto Text to Speech with Function Call")

# Input text box
text_input = st.text_input("Enter text:")

# Trigger the function to convert text to speech
if text_input:
    speak(text_input)
    st.write(f"Speaking: {text_input}")
