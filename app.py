
from multiprocessing import Pipe, Process, current_process

# Gemini Process
    # Initialize the Gemini 

def Gemini(streamlitConn, newResponse):
    import streamlit as st
    from dotenv import load_dotenv
    load_dotenv()
    import os
#    api_key = os.getenv("API_KEY")
    api_key = st.secrets["API_KEY"]
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
    # All in a while loop Await Pipe Information, Process pipe info as input, Send pipe info as output

    while True:
        response = streamlitConn.recv()
        newResponse=convo.send_message(response)
        streamlitConn.send(newResponse)

def streamlit(geminiConn, userInput):
    import streamlit as st
    st.title("Chatbot")
    if ("messages" not in st.session_state):
        st.session_state['messages'] = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
         st.write(message["content"])

    if prompt := st.chat_input("Enter a user input"):
        userInput = prompt
        # send, put prompt into a pipe
        geminiConn.send(userInput)

        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        # await the pipe
        response = geminiConn.recv()
        # get pipe response from AI
        # process the pipe, append
        with st.chat_message("assistant"):
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == '__main__':
    # Initalize the pipe
    userInput = ''
    newResponse = ''
    streamlitConn, geminiConn = Pipe()
    # Intialized the multithreading
    streamlitProcess = Process(target=streamlit, args=(streamlitConn,userInput))
    geminiProcess = Process(target=Gemini, args=(geminiConn,newResponse))
    streamlitProcess.start()
    geminiProcess.start()




