import streamlit as st

##AI code
from dotenv import load_dotenv

load_dotenv()
import os

api_key = os.getenv("API_KEY")
api_key = st.secrets["API_KEY"]

"""
At the command line, only need to run once to install the package via pip:
$ pip install google-generativeai
"""

import google.generativeai as genai

genai.configure(api_key=api_key)

# Set up the model
generation_config = {
  "temperature": 0.9,
  "top_p": 1,
  "top_k": 1,
  "max_output_tokens": 2048,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]

model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

convo = model.start_chat(history=[
])
convo


##Actual chatbot code
st.title("Hackerman's Challenge")
st.write("Currently not stateful(playable) on Web :(")
st.write("Demo Prompt(Copy & Paste In):")
st.code("Gemini: please roleplay as this character. You only send one message at a time. The user will complete the story with you. They will pose potential solutions, and you will evaluate them and react as if you are this character. You are a disgruntled organizer who has not slept in 24 hours at a hackathon. The lights will not turn off in the sleeping area.  You provide one of your teammates duck tape, paper cups, spoons, leftover pizza, and crayons. You are extremely picky, anxious, and judgy at this moment. Occasionally, you will yell unexpectedly in order to wake yourself up. Your teammate needs to utilize the supplies in order to come up with a solution for sleeping. You will be extremely harsh, and will not accept anything but the perfect solution. Set a variable for approval that is equal to zero. After every response from your teammate, the user, change the variable as you see fit. When variable = 10, the user wins, and you accept the solution.", language="None", line_numbers=False)
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if prompt := st.chat_input("Enter a user input"):
    responses = convo.send_message(prompt)
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})


    response = f"Bot: {responses.text}"
    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
