import streamlit as st
import classify_diagnosis
from streamlit_lottie import st_lottie
import json
import time

# Настройка страницы
st.set_page_config(page_title="SharkLab Assistant", page_icon="🦈", layout="wide")

#фон страницы
pg_bg_img = """
    <style>
    [data-testid="stAppViewContainer"] { 
    width: 100%;
    height: 100%;
    background-size: 1500px 700px;
    background-position: center center;
    background-repeat: no-repeat;
    background-image: url("https://i.pinimg.com/736x/7a/84/66/7a8466e4d1bfa445f15c4ccc44cf5f62.jpg");}
    [data-testid="stHeader"] { 
    background-color: rgba(0, 0, 0, 0);
    </style>
    """
st.markdown(pg_bg_img,unsafe_allow_html=True)

# CSS-стили для размещения элементов
st.markdown(
    """
    <style>
    .info-box {
        background-color: #ffffff;
        border: 1px solid #A4D7F7;
        padding: 20px 60px;
        border-radius: 10px;
        font-size: 14px;
        color: #15aabf;
    }
    .stButton>button {
                background-color: #0c8599; /* цвет кнопки */
                color: #a5a5a5; /* цвет текста */
                padding: 20px 80px; /* размер кнопки */
                font-size: 30px; /* размер текста */
                border-radius: 10px; /* закругление углов */
            }
    </style>
    """,
    unsafe_allow_html=True,
)

# Две колонки: текст справа, изображение слева
col1, col2 = st.columns([1, 1], vertical_alignment="center")
#Текст результата
with col1:
    with st.spinner("Наши акульи мозги заработали на полную... ждем результатов!✨🦈"):
        time.sleep(10)
        try:
            form_id = st.session_state['user_form_id']
            label =  classify_diagnosis.diagnosis_classifier(form_id)
            st.success(label)
        except KeyError:
                st.error("Упс, наши акульи сенсоры не обнаружили результатов... 🦈💦")
        except Exception as e:
                st.error(f"Мы извиняемся, кажется, наши акульи сенсоры запутались в потоке данных... 🦈💧 🙇 {e}")
    
        if st.button("Хочешь заполнить еще раз?"):
            st.switch_page("pages/2_form.py")
#Изображение
with col2:
    st.image("images/image2.png", width=450, use_container_width=False)

    
