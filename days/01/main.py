import streamlit as st
import llm_gen as ai

st.title("LLM Sandboxing for Prompt Engineering Challenge🧪")
st.text("A sandbox created by Abdallah ")

def call_ai():
    response = ai.invoke_ai(system_prompt, user_input, ai_mood, ai_language, temperature, model)
    with st.chat_message("assistant"):
        st.markdown(response)

### SIDE BAR ###
with st.sidebar:
    st.subheader("LLM model")
    model = st.selectbox(
        "Select a model",
        ("llama3.1","mistral") #Change these depending of the LLMs you have installed on Ollama
    )

    st.subheader("Temperature:")
    temperature = st.slider(
        "Choose between 0.0 and 1.0",
        min_value=0.0,
        max_value=1.0,
        step=0.1,
        value=0.5
        )
    st.subheader("System Prompt")
    system_prompt = st.text_area(
        "Write a System Prompt",
        ""
    )
    st.subheader("User")
    user_input = st.text_area(
        "Write a User task",
        ""
    )

    st.subheader("Mood Response")
    ai_mood = st.selectbox(
        "Select a mood",
        ("Happy","Sad","Nervous","Angry","Stingy","Dumb")
    )

    st.subheader("Laguage")
    ai_language = st.text_input(
        "Mood Response",
        "English"
    )

if st.button("Test Response"):
    with st.spinner("Generating response..."):
        call_ai()