import pyttsx3
import random
import string
import smtplib
import re
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import streamlit as st
import os
from streamlit_option_menu import option_menu
from Stsocialicon import SocialMediaIcons
import pandas as pd
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
#for title
def title():
    st.set_page_config(page_title="IAA",layout="wide",page_icon='media/logo.png')
    user_color      = '#000000'
    title_webapp    = "IAA-I AM AVAILABLE"

    html_temp = f"""
                <div style="background-color:{user_color};padding:12px">
                <h1 style="color:white;text-align:center;font-size: 38px;">{title_webapp}</h1>
                </div>
                """
    st.markdown(html_temp, unsafe_allow_html=True)

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

##################################################################################
##Contact us 
def contact():
    st.subheader("Contact us Form")
    with st.form("contact_form", clear_on_submit=True):
            contact_name = st.text_input("Enter your name")
            contact_email = st.text_input("Enter your email address")
            contact_message = st.text_area("Enter your message")
            contact_submit = st.form_submit_button("Send Message")
            if contact_submit:
                if not contact_name or not contact_email or not contact_message:
                    st.error("Please fill in all required fields.")
                elif not re.match(r"[^@]+@[^@]+\.[^@]+", contact_email):
                    st.error("Please enter a valid email address.")
                else:
                    st.success(f"Thank you, {contact_name}! Your message has been sent.")
    select = option_menu("MEET OUR TEAM", 
        ['Team','Individual'],
        icons=['people', 'person-bounding-box'],
        menu_icon="microsoft-teams", default_index=0,orientation="horizontal")
    if select == 'Team':
        st.image('media/team.jpg',use_column_width=True,caption='team image')
        st.write("""fhsdgjiohsdfjihgjihsjihfgjhsjhjifhdjgsdhfgshndjfghjishfjghjfhgjkhjkfjhgjksdfgjhsdjhfgjkhsdfjkghjsdhfgusuidjghsuihgifnjsdfhjghsduighjnjhuidvdsnfuvhuifnvijsvhnjisunfhisdnviufhsdnvifbhsdfjvisdbfivbsbsdbbsdfjiisdhfjgnsdfihgjnsdfjhgjsdhjghjsdngjhsdjghjsdnfvhsdfjbvsdjibhjnrfjivbsjdfbhvsdjirgbjsdhfjignnkvbhsrjiegvsdrhjinfdjksvihuisdnvjinjkfbhsdkr
                """)
    if select == 'Individual':
        data_df  = pd.DataFrame(
               data = {
        "Name": ["Sumit Kumar Singh", "Mantu Rana", "Mayank Pathak", "Madan HS"],
        "LinkedIn": [
            "https://www.linkedin.com/in/sumit-singh-773921262/",
            "https://www.linkedin.com/in/mantu-kumar-rana-71a6ba25b/",
            "https://www.linkedin.com/in/mayank-pathak-46168a281/",
            ""
        ],
        "GitHub": [
            "https://github.com/RAJPUTRoCkStAr",
            "https://github.com/MantuRana",
            "https://github.com/MayankPathak13/Internship_AI.git",
            "https://github.com/Madanedunet"
        ],
        "apps": [
            "media/resized_sumitimg.jpg",
            "media/resized_mantuimg.jpg",
            "media/resized_mayankimg.jpg",
            "media/resized_madanimg.jpg"
        ]
        }
        )
        st.header('Team Individual Profiles')
        edited_df = st.data_editor(
        data_df,
        column_config={
        "apps": st.column_config.ImageColumn(
            "Preview Image", help="Streamlit app preview screenshots"
        ),
        "LinkedIn": st.column_config.LinkColumn(
            "LinkedIn Profile", help="Edit LinkedIn URL",display_text="LinkedIn Profile"
        ),
        "GitHub": st.column_config.LinkColumn(
            "GitHub Profile", help="Edit GitHub URL",display_text="GitHub Profile"
        )
        },
        hide_index=True,use_container_width=True
        )
