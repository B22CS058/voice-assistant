# import streamlit as st
# import speech_recognition as sr
# from gtts import gTTS
# import os
# import google.generativeai as genai

# # Configure Gemini API (replace with your actual API key)
# genai.configure(api_key="AIzaSyBXouquUMxC-acLs4HK5ajIMgaQX06R630")

# # Function to transcribe audio
# def transcribe_audio(audio_file_path):
#     recognizer = sr.Recognizer()
#     with sr.AudioFile(audio_file_path) as source:
#         audio_data = recognizer.record(source)
#         try:
#             text = recognizer.recognize_sphinx(audio_data)
#             return text
#         except Exception as e:
#             return f"Error: {e}"

# # Function to generate response with chat history
# def generate_response(chat_history):
#     # Convert chat history to the required format (exclude the latest user message)
#     history = []
#     for msg in chat_history[:-1]:
#         role = "user" if msg['role'] == 'user' else "model"  # Map 'assistant' to 'model'
#         history.append({"role": role, "parts": [msg['content']]})
    
#     # Initialize the model and start a chat session with the history
#     model = genai.GenerativeModel('gemini-2.0-flash-thinking-exp')  # Replace with the correct model name if needed
#     chat = model.start_chat(history=history)
    
#     # Send the latest user message to get the response
#     response = chat.send_message(chat_history[-1]['content'])
#     return response.text

# # Function to convert text to speech
# def text_to_speech(text, output_file):
#     tts = gTTS(text=text, lang='en')
#     tts.save(output_file)

# # --- Streamlit UI ---

# # Birthday Decorations
# st.markdown("""
# <style>
# .balloons {
#   font-size: 50px;
#   animation: float 3s ease-in-out infinite;
# }
# @keyframes float {
#   0%, 100% { transform: translateY(0); }
#   50% { transform: translateY(-20px); }
# }
# </style>
# <div class='balloons'>
# 🎈🎈🎈🎂🎉🎈🎈🎈
# </div>
# """, unsafe_allow_html=True)

# st.markdown("""
# <h1 style='color: #ff4081; text-align: center;'>Happy Birthday! 🎉🎂🎈</h1>
# """, unsafe_allow_html=True)

# # Play Happy Birthday Audio if available
# if os.path.exists("happy_birthday.mp3"):
#     with open("happy_birthday.mp3", "rb") as audio_file:
#         audio_bytes = audio_file.read()
#     st.audio(audio_bytes, format='audio/mp3', start_time=0)

# # Initialize chat history in session state
# if 'chat_history' not in st.session_state:
#     st.session_state.chat_history = []

# # User Input
# user_input = st.text_input("Type your message here:")
# audio_file = st.file_uploader("Or upload an audio file (WAV format)", type=["wav"])

# # Handle Response Generation
# if st.button("Get Response"):
#     if user_input or audio_file:
#         if audio_file:
#             # Save and transcribe the uploaded audio
#             with open("temp.wav", "wb") as f:
#                 f.write(audio_file.read())
#             input_for_response = transcribe_audio("temp.wav")
#             os.remove("temp.wav")
#         else:
#             input_for_response = user_input

#         # Add the user message to chat history
#         st.session_state.chat_history.append({'role': 'user', 'content': input_for_response})

#         # Generate response using the entire chat history
#         response_text = generate_response(st.session_state.chat_history)

#         # Add assistant response to chat history
#         st.session_state.chat_history.append({'role': 'assistant', 'content': response_text})

#         # Convert response to speech and play it
#         output_file = "response.mp3"
#         text_to_speech(response_text, output_file)
#         st.audio(output_file, format='audio/mp3')
#         os.remove(output_file)
#     else:
#         st.warning("Please type a message or upload an audio file.")

# # Display Chat History
# st.markdown("## Chat History")
# for chat in st.session_state.chat_history:
#     if chat['role'] == 'user':
#         st.markdown(f"**You:** {chat['content']}")
#     else:
#         st.markdown(f"**Assistant:** {chat['content']}")





import streamlit as st
import speech_recognition as sr
from gtts import gTTS
import os
import google.generativeai as genai
from streamlit_mic_recorder import mic_recorder

# Configure Gemini API (replace with your actual API key)
genai.configure(api_key="AIzaSyBXouquUMxC-acLs4HK5ajIMgaQX06R630")

def transcribe_audio(audio_data, sample_rate=16000, sample_width=2):
    """Transcribe audio data (WAV bytes) using SpeechRecognition"""
    recognizer = sr.Recognizer()
    audio = sr.AudioData(audio_data, sample_rate, sample_width)
    try:
        # Using Sphinx for offline transcription; switch to recognize_google for better accuracy if online
        text = recognizer.recognize_sphinx(audio)
        return text
    except Exception as e:
        return f"Error transcribing audio: {e}"

def generate_response(chat_history):
    """Generate a response using Gemini with chat history"""
    history = []
    for msg in chat_history[:-1]:
        role = "user" if msg['role'] == 'user' else "model"  # Map 'assistant' to 'model'
        history.append({"role": role, "parts": [msg['content']]})
    model = genai.GenerativeModel('gemini-2.0-flash-thinking-exp')  # Replace with the correct model name if needed
    chat = model.start_chat(history=history)
    response = chat.send_message(chat_history[-1]['content'])
    return response.text

def text_to_speech(text, output_file="response.mp3"):
    """Convert text to speech and save as MP3"""
    tts = gTTS(text=text, lang='en')
    tts.save(output_file)
    return output_file

# --- Streamlit UI ---

# Birthday Decorations
st.markdown("""
<style>
.balloons {
  font-size: 50px;
  animation: float 3s ease-in-out infinite;
}
@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-20px); }
}
</style>
<div class='balloons'>
🎈🎈🎈🎂🎉🎈🎈🎈
</div>
""", unsafe_allow_html=True)
st.markdown("""
<h1 style='color: #ff4081; text-align: center;'>Happy Birthday! 🎉🎂🎈</h1>
""", unsafe_allow_html=True)

# Play Happy Birthday Audio if available
if os.path.exists("happy_birthday.mp3"):
    with open("happy_birthday.mp3", "rb") as audio_file:
        audio_bytes = audio_file.read()
    st.audio(audio_bytes, format='audio/mp3', start_time=0)

# Initialize chat history in session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Streamlit app layout
st.title("Your personal chatbot")

# Radio button to select input method
input_method = st.radio("Select input method:", ["Type a message", "Upload audio file", "Record audio"])

user_input = None
input_for_response = None

# Display input widget based on selected method
if input_method == "Type a message":
    user_input = st.text_input("Type your message here:")
elif input_method == "Upload audio file":
    audio_file = st.file_uploader("Upload an audio file (WAV format)", type=["wav"])
    if audio_file is not None:
        audio_data = audio_file.read()
        input_for_response = transcribe_audio(audio_data)
elif input_method == "Record audio":
    st.info("Please allow microphone access when prompted by your browser.")
    recorded_audio = mic_recorder(start_prompt="Start Recording", stop_prompt="Stop Recording")
    if recorded_audio and 'bytes' in recorded_audio:  # Use 'bytes' key, not 'audio_bytes'[4][5]
        input_for_response = transcribe_audio(recorded_audio['bytes'])

# Handle Response Generation
if st.button("Chat"):
    if input_method == "Type a message" and user_input:
        input_for_response = user_input
    if input_for_response:
        # Add the user message to chat history
        st.session_state.chat_history.append({'role': 'user', 'content': input_for_response})
        # Generate response using the entire chat history
        response_text = generate_response(st.session_state.chat_history)
        # Add assistant response to chat history
        st.session_state.chat_history.append({'role': 'assistant', 'content': response_text})
        # Convert response to speech and play it
        output_file = text_to_speech(response_text)
        st.audio(output_file, format='audio/mp3')
        os.remove(output_file)
    else:
        st.warning("Please type a message, upload an audio file, or record audio.")

# Display Chat History
st.markdown("## Our conversations")
for chat in st.session_state.chat_history:
    if chat['role'] == 'user':
        st.markdown(f"**You:** {chat['content']}")
    else:
        st.markdown(f"**Me:** {chat['content']}")
