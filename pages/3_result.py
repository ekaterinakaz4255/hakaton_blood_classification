import streamlit as st
from streamlit_lottie import st_lottie
import json

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
#Текс
with col1:
    st.markdown(
        """
        <div class="info-box">
           <h2 align="center"><b>Акулье одобрение!</b></h2> 
           <h3 align="center">Но для ещё более бодрого плавания по жизни советую заглянуть к врачу на 
           плановый осмотр и поработать над весом с помощью питания и упражнений!</h3>
        </div>
        """,
        unsafe_allow_html=True,
    )
#Изображение
with col2:
    st.image("images/image2.png", width=450, use_container_width=False)

st.write("")
col3, col4, col5 = st.columns([1, 1, 1])
with col4:
    if st.button("Хочешь заполнить еще раз?"):
        st.switch_page("pages/2_form.py")
