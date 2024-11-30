import streamlit as st
from streamlit_lottie import st_lottie
import time

# Настройка страницы
st.set_page_config(page_title="SharkLab Assistant", page_icon="🦈", layout="wide")

#Переназвать страницы (не переходит по страницам)
# rules = st.Page('str.py', title='Предупреждение', icon=":material/add_circle:")
# form_oak = st.Page('pages/2_form.py', title='Форма ввода данных', icon=":material/add_circle:")
# pg = st.navigation([rules, form_oak])

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
        padding: 10px 80px;
        border-radius: 10px;
        font-size: 25px;
        color: #15aabf;
    }
    .stButton>button {
                background-color: #0c8599; /* цвет кнопки */
                color: #a5a5a5; /* цвет текста */
                padding: 20px 80px; /* размер кнопки */
                font-size: 30px; /* размер текста */
                border-radius: 10px; /* закругление углов */
            }
    }
    .stImage>image {
                    float: right;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Две колонки: текст справа, изображение слева
col1, col2 = st.columns([1, 1], vertical_alignment="center")
#Текс
with col2:
    st.markdown(
        """
        <div class="info-box">
        <h3>Привет!</h3>
        <p>Меня зовут Блуди, рад знакомству! Я — акула-гематолог из SharkLab.</p> 
        <p>Хочешь помогу тебе расшифровать твой общий анализ крови?</p>
           <p ><b><u>Только не забывай:</u></b> я тут, чтобы объяснять и рассказывать, но не лечить! 
            Мои советы не заменяют консультацию врача, и я не могу поставить диагноз. 
            Вся информация, которую я даю, предназначена только для образовательных целей 
            и не является медицинской консультацией. Используя мои услуги, ты признаёшь, 
            что ответственность за их применение остается на тебе.</p> 
        <p>Пожалуйста, внимательно читай мои сообщения и помни, 
        что для точного лечения всегда нужен профессиональный врач!</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
#Изображение
with col1:
    st.image("images/image2.png", width=450, use_container_width=False)

#Кнопка
#Надо допилить переключение по ней на следующую страницу и подлючение анимации загрузки
st.write("")
col3, col4, col5 = st.columns([1, 1, 1])
with col4:
    if st.button("Да, я согласен! Идем дальше."):
        st.switch_page("pages/2_form.py")


