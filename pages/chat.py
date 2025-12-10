import streamlit as st
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEYS"])


st.title("Chat with GPT-5.1")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


prompt = st.chat_input("You: ")

if prompt:
    st.session_state.message.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar=""):
        st.markdown(prompt)

completion = client.chat.completions.create(
    model="gpt-5.1",
    messages=st.session_state.messages
    )

with st.chat_message("assistant"):
    response = completion.choices[0].message.content
    st.markdown(response)
    st.session_state.message.append({"role": "assistant", "content": response})
