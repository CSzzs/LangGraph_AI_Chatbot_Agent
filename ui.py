import streamlit as st
import requests

st.set_page_config(page_title="LangGraph AI Agent", page_icon="🤖", layout="centered")

#Define API endpoint
API_URL = "http://127.0.0.1:8000/chat"

#Predifine models
MODEL_NAMES =[
    "llama3-70b-8192",
    "mixtral-8x7b-32768"
]

#Streamlit UI Elements
st.title("LangGraph AI Chatbot Agent 🤖")
st.write("Interact with the LangGraph based agent using this interface.")

#Input box for system prompt
given_system_prompt = st.text_area("Define your AI Agent 🤖", height=70, placeholder="Type your system prompt here...")

#Dropdown for selecting the model
selected_model = st.selectbox("Select the model to use", MODEL_NAMES)

#input box for user messages
user_inputs = st.text_area("Type your messages here", height=150, placeholder="Type your messages here...")

#Button for sending the request
if st.button("Send Query"):
    if user_inputs.strip():
        try:
            #send the input to the fastapi backend
            payload = {'messages':[user_inputs], "model_name":selected_model, "system_prompt":given_system_prompt}
            response = requests.post(API_URL, json=payload)

            #Display the response
            if response.status_code == 200:
                response_data = response.json()
                if 'error' in response_data:
                    st.error(response_data['error'])
                else:
                    ai_response = [
                        message.get("content", "")
                        for message in response_data.get("messages",[])
                        if message.get("type") == "ai"
                    ]

                    if ai_response:
                        st.subheader("Agent Response:")
                        st.markdown(f"**Final Response:** {ai_response[-1]}")
                        #for i, response_text in enumerate(ai_response, 1):
                        #    st.markdown(f"**Response** {i}: **{response_text}"**)
                    else:
                        st.warning('No AI response found in the agent output.')
            else:
                st.error(f"Request Failed with status code {response.status_code}.")
        except Exception as e:
            st.error(f"an error occured: {e}")
    else:
        st.warning("please enter a message before clicking  'send query' button.")