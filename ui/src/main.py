import os
import requests
import streamlit as st

CHATBOT_URL = os.getenv("CHATBOT_URL", "http://chatbot_api:8000/math-rag-agent")

with st.sidebar:
    st.header("Інформація")
    st.markdown(
        """
        Зроблено на основі LangChain за допомогою Streamlit, з любовʼю 
        """
    )

    st.header("Приклади запитів:")
    st.markdown("Ортогональність")
    st.markdown("Розклад Матриць")
    st.markdown("Матриці")
    st.markdown("Обернені Матриці")
 
st.title("РепетиторGPT")
st.info(
    "Бот який готує до екзамену з лінійної алебри "
)

if "messages" not in st.session_state:
    st.session_state.messages = []
    
if prompt := st.chat_input("Виберіть тему на яку хочете підготуватись?"):
    st.chat_message("user").markdown(prompt)

    st.session_state.messages.append({"role": "user", "output": prompt})

    data = {"question": prompt}

    with st.spinner("Готую відповіді..."):
        print("data", data)
        response = requests.post(CHATBOT_URL, json=data)

        if response.status_code == 200:
            questions = response.json()["answer"] 
            answers = response.json()["wolfram_answer"]
        else:
            questions = """Сталася помилка, переробіть свій запит будь ласка"""
            explanation = questions

    st.chat_message("assistant").markdown(questions)
    st.chat_message("assistant").markdown(answers)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "output": questions,
        }
    )
    
    st.session_state.messages.append(
        {
            "role": "assistant",
            "output": answers,
        }
    )

