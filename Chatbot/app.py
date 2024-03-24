import os
import streamlit as st
from dotenv import load_dotenv
from streamlit_option_menu import option_menu
from PIL import Image
import google.generativeai as genai

# load environment variables
load_dotenv()

GOOGLE_API_KEY = os.getenv("api_key")
print(GOOGLE_API_KEY)

# setup google gemeini-pro ai model
genai.configure(api_key=GOOGLE_API_KEY)

def gemini_pro():
    model = genai.GenerativeModel('gemini-pro')
    return model

def gemini_vision():
    model = genai.GenerativeModel('gemini-pro-vision')
    return model

def gemini_vision_response(model, prompt, image):
    response = model.generate_content([prompt, image])
    return response.text

st.set_page_config(
    page_title="Chat with Gemi",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="expanded"
)

with st.sidebar:
    user_picked = option_menu(
        "Google Gemini AI",
        ["Chatbot", "Image Captioning"],
        menu_icon="robot",
        icons = ["chat-dots-fill", "image-fill"],
        default_index=0
    )
    

def roleforStreamlit(user_role):
    if user_role == 'model':
        return 'assistant'
    else:
        return user_role
    
if user_picked == 'Chatbot':
    model = gemini_pro()

    if "chat_history" not in st.session_state:
        st.session_state['chat_history'] = model.start_chat(history=[])

    st.title("🤖TalkBot")

    for message in st.session_state['chat_history'].history:
        with st.chat_message(roleforStreamlit(message.role)):
            st.markdown(message.parts[0].text)
    
    user_input = st.chat_input("Message TalkBot: ")
    if user_input:
        st.chat_message("user").markdown(user_input)
        response = st.session_state['chat_history'].send_message(user_input)
        with st.chat_message("assistant"):
            st.markdown(response.text)
        

if  user_picked == 'Image Captioning':
    model = gemini_vision()

    st.title("🖼️Image Captioning")

    image = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])

    user_prompt = st.text_input("Enter the prompt for image captioning:")

    if st.button("Generate Caption"):
        load_image = Image.open(image)

        colLeft, colRight = st.columns(2)

        with colLeft:
            st.image(load_image.resize((800, 500)))
        
        caption_response = gemini_vision_response(model, user_prompt, load_image)

        with colRight:
            st.info(caption_response)



