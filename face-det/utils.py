import pyttsx3
import random
import string
import smtplib
import re
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import streamlit as st
import os
################################################################
#text-to-speech
def tts(text):
    engine =  pyttsx3.init()
    rate = engine.getProperty('rate')
    engine.setProperty('rate', 175)                
    engine.say(text)
    engine.runAndWait()

####################################################################

####################################################################
#generate username
def generate_username(name):
    base_name = name.lower().replace(' ', '')
    random_suffix = ''.join(random.choices(string.digits, k=4))
    username = f"{base_name}{random_suffix}"
    return username

######################################################################

######################################################################







######################################################################





######################################################################
#Sign up mail sending
def send_thank_you_email(email, username, password, job_role, item, place_name):
    try:
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        smtp_username = os.getenv('SMTP_USERNAME')
        smtp_password = os.getenv('SMTP_PASSWORD')
        message = MIMEMultipart()
        message['From'] = smtp_username
        message['To'] = email
        message['Subject'] = 'Welcome to Our Platform!'
        html = f"""
        <html>
        <body>
            <div style="font-family: Arial, sans-serif; color: #333;">
                <h1 style="color: #1a73e8;">Welcome, {username}!</h1>
                <p>Thank you for registering with us. We're excited to have you on board!</p>
                <p>Your username: <strong>{username}</strong></p>
                <p>Your password: <strong>{password}</strong></p>
                <p>Your job role: <strong>{job_role} in {item}</strong></p>
                <p>Your place of work: <strong>{place_name}</strong></p>
                <p>To get started, you can now log in with your credentials and explore the platform.</p>
                <p>Best regards,<br>The Team</p>
                <hr style="border: 0; border-top: 1px solid #ddd;" />
                <footer>
                    <p style="font-size: 0.9em; color: #777;">
                        &copy; 2024 Our Company IAA. All rights reserved.<br>
                        <a href="http://example.com" style="color: #1a73e8; text-decoration: none;">Visit our website</a>
                    </p>
                </footer>
            </div>
        </body>
        </html>
        """
        message.attach(MIMEText(html, 'html'))
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.send_message(message)
        st.success(f"Congratulations, {username}! Your registration as a {job_role} in {place_name} is now complete. An email with your login credentials has been sent to {email}. Please check your inbox to access your account and start using our services.")
        tts(f"Congratulations, {username}! Your registration as a {job_role} in {place_name} is now complete. An email with your login credentials has been sent to {email}. Please check your inbox to access your account and start using our services.")
    except Exception as e:
        st.error(f"Failed to send email: {e}")

#####################################################################