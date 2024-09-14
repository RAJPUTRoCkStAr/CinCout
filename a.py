# import streamlit as st
# from gtts import gTTS
# from io import BytesIO

# def main():
#     st.title('Text-to-Speech with Streamlit')

#     text = st.text_area("Enter text to convert to speech:")
    
#     if st.button('Generate Speech'):
#         if text:
#             tts = gTTS(text=text, lang='en')
#             audio_bytes = BytesIO()
#             tts.write_to_fp(audio_bytes)
#             audio_bytes.seek(0)
            
#             st.audio(audio_bytes, format='audio/mp3')
#         else:
#             st.error("Please enter some text.")

# if __name__ == "__main__":
#     main()
import streamlit as st
from PIL import Image
from pyzbar.pyzbar import decode

def main():
    st.title("QR Code Reader")

    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # Open the image file
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Image.', use_column_width=True)
        
        # Decode the QR code
        decoded_objects = decode(image)
        
        if decoded_objects:
            for obj in decoded_objects:
                st.write(f"QR Code Data: {obj.data.decode('utf-8')}")
        else:
            st.write("No QR code detected.")

if __name__ == "__main__":
    main()
