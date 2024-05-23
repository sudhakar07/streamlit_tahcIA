import openai
import streamlit as st

st.title("Gen-AI ChatBot")


openai.api_key = st.secrets["OPENAI_API_KEY"]
api_key_secrectpass = st.secrets["OPENAI_API_PASS"]

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            #viewerBadge_link__qRIco {visibility: hidden;}
            viewerBadge_link__qRIco {visibility: hidden;}
            </style>
           
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

name = st.text_input("Enter your SecretPass (required)", type="password")
st.warning(name)
st.warning(api_key_secrectpass)

#if name=="Hi":
  #st.warning("Please fill out so required fields")

if name == api_key_secrectpass:
   if "openai_model" not in st.session_state:
       openai.api_key = st.secrets["OPENAI_API_KEY"]
       st.session_state["openai_model"] = "gpt-3.5-turbo"
   else:
       openai.api_key = ""
       st.session_state["openai_model"] = ""
            

    
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for response in openai.ChatCompletion.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        ):
            full_response += response.choices[0].delta.get("content", "")
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})
