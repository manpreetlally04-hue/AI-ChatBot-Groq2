import streamlit as st
from groq import Groq

st.title("Llama chat bot")
st.caption("Cloud AI Chatbot using Groq API")

# Automatically reads from st.secrets when deployed to the cloud
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

prompt = st.chat_input("Write Something")

if prompt:
    with st.chat_message("user"):
        st.write(prompt)

    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        try:
            # Using the active replacement model ID as per Groq specifications
            response = client.chat.completions.create(
                model="openai/gpt-oss-20b", 
                messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
                stream=True,
            )

            def stream_generator():
                for chunk in response:
                    # Added [0] index to read from the choices list correctly
                    if chunk.choices and chunk.choices[0].delta.content is not None:
                        yield chunk.choices[0].delta.content

            full_response = st.write_stream(stream_generator())
            st.session_state.messages.append({"role": "assistant", "content": full_response})

        except Exception as e:
            st.error(f"Failed to connect to AI service: {e}")
