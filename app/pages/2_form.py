import streamlit as st
import sqlalchemy
from sqlalchemy.orm import Session
import datetime
import pandas as pd
import time

# Настройка страницы
st.set_page_config(page_title="SharkLab Assistant", page_icon="🦈", layout="wide")

# db conn
#conn = st.connection('gbd', type='sql')
sql_engine = sqlalchemy.create_engine('sqlite:///data/gbd.db', echo=False)
conn = sql_engine.raw_connection()

@st.cache_resource
def get_database_session():
    # Create a database session object that points to the URL.
    return Session(sql_engine)

# CSS-стили для размещения элементов
st.markdown(
    """
    <style>
    .info-box {
        background-color: #ffffff;
        border: 1px solid #A4D7F7;
        padding: 20px 10px;
        border-radius: 10px;
        font-size: 14px;
        color: #15aabf;
        position: absolute; 
        left: 40%;
        margin-top: -20%;  
        transform: translateX(0%);
    }
    .stButton>button {
                background-color: #0c8599; /* цвет кнопки */
                color: #a5a5a5; /* цвет текста */
                padding: 20px 170px; /* размер кнопки */
                font-size: 30px; /* размер текста */
                border-radius: 10px; /* закругление углов */
            }
    }
    .stImage>image {
                    position: absolute;
                    right: 50px;
                    top: 50%;
                    transform: translateY(-70%);
    }
    </style>
    """,
    unsafe_allow_html=True,
)
#Акула с инфо блоком + инфа про *
col1, col2 = st.columns(2, vertical_alignment="center")
#Текст
with col1:
    st.markdown(
            """
            <div class="info-box">
            <p>Тогда заполни, пожалуйста, поля с показателями из своего бланка анализа ОАК (общего анализа крови).</p>
            <p>Поля, отмеченные звездочкой, обязательны для заполнения.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    #Изображение
with col2:
    st.image("images/sticker.png", width=300, use_container_width=False)
# Две колонки: текст справа, изображение слева
with st.form(key='gbd'):
    #Блок личная информация
    st.markdown(
        """
        <div class="personal-info">
        <style>.personal-info {
            background-color: #ffffff;
            padding: 20px 10px;
            font-size: 14px;
            color: #15aabf;
            text-align: center
        }</style>
        <h2> Личная информация </h2>
        </div>
        """,
        unsafe_allow_html=True,
    )
    col1, col2 = st.columns([1, 1])
    
    #Форма для ввода пола и даты рождения
    with col1:
        gender = st.selectbox("Пол: *", ["Мужской", "Женский"])
        date_of_birth = st.date_input("Дата рождения: *", value=None, min_value=datetime.date(1900, 1, 1), max_value=datetime.date.today())

    #Форма для ввода роста и веса
    with col2:
        height = st.number_input("Рост (см):", value=None, min_value=0, max_value=250)
        weight = st.number_input("Вес (кг):", value=None, min_value=0, max_value=300)

    #Блок параметров ОАК
    st.markdown(
        """
        <div class="personal-info">
        <style>.personal-info {
            background-color: #ffffff;
            padding: 20px 10px;
            font-size: 14px;
            color: #15aabf;
            text-align: center
        }</style>
        <h2> Параметры ОАК </h2>
        </div>
        """,
        unsafe_allow_html=True,
    )

    #Формы для ввода параметров ОАК обязательные
    st.markdown(
        """
        <div class="personal-info">
        <style>.personal-info {
            background-color: #ffffff;
            padding: 20px 10px;
            font-size: 14px;
            color: #15aabf;
            text-align: left
        }</style>
        <h3> Обязательные параметры </h3>
        </div>
        """,
        unsafe_allow_html=True,
    )
    col3, col4, col5 = st.columns([1, 1, 1])
    with col3:
        wbs = st.number_input("Лейкоциты (WBC): *", value=None, min_value=0.0, max_value=1000.0, step=0.1, format="%.1f")
        rbs = st.number_input("Эритроциты (RBC): *", value=None, min_value=0.0, max_value=1000.0, step=0.1, format="%.1f")
        plt = st.number_input("Трмбоциты (PLT): *", value=None, min_value=0.0, max_value=1000.0, step=0.1, format="%.1f")
        hct = st.number_input("Гематокрит (HCT): *", value=None, min_value=0.0, max_value=1000.0, step=0.1, format="%.1f")
        hgb = st.number_input("Гемоглобин (HGB): *", value=None, min_value=0.0, max_value=1000.0, step=0.1, format="%.1f") 
   
    with col4:
        mcv = st.number_input("Средний объем эритроцита (MCV): *", value=None, min_value=0.0, max_value=1000.0, step=0.1, format="%.1f")
        mch = st.number_input("Среднее содержание гемоглобина в эритроците (MCH): *", value=None, min_value=0.0, max_value=1000.0, step=0.1, format="%.1f")
        mchc = st.number_input("Уровень концентрации гемомоглобина в эритроцитах (MCHC): *", value=None, min_value=0.0, max_value=1000.0, step=0.1, format="%.1f")

    with col5:
        ly_abs = st.number_input("Лимфоциты # (LY#): *", value=None, min_value=0.0, max_value=1000.0, step=0.1, format="%.1f")
        mo_abs = st.number_input("Моноциты # (MO#): *", value=None, min_value=0.0, max_value=1000.0, step=0.1, format="%.1f")
        ne_abs = st.number_input("Нейтрофилы # (NE#): *", value=None, min_value=0.0, max_value=1000.0, step=0.1, format="%.1f")
        eo_abs = st.number_input("Эозинофилы # (EO#): *", value=None, min_value=0.0, max_value=1000.0, step=0.1, format="%.1f")
        ba_abs = st.number_input("Базофилы # (BA#): *", value=None, min_value=0.0, max_value=1000.0, step=0.1, format="%.1f")


    #Необязательные параметры
    st.markdown(
        """
        <div class="personal-info">
        <style>.personal-info {
            background-color: #ffffff;
            padding: 20px 10px;
            font-size: 14px;
            color: #15aabf;
            text-align: left
        }</style>
        <h3> Опциональные параметры </h3>
        </div>
        """,
        unsafe_allow_html=True,
    )
    col6, col7, col8= st.columns([1, 1, 1])
    with col6:
        pct = st.number_input("Тромбокрит (PCT):", value=None, min_value=0.0, max_value=1000.0, step=0.1, format="%.1f")
        mpv = st.number_input("Средний объем тромбоцита (MPV):", value=None, min_value=0.0, max_value=1000.0, step=0.1, format="%.1f")
        pdw = st.number_input("Распределение тромбоцитов по объему (PDW):", value=None, min_value=0.0, max_value=1000.0, step=0.1, format="%.1f")
        rdw = st.number_input("Распределение эритроцитов по объему (RDW):", value=None, min_value=0.0, max_value=1000.0, step=0.1, format="%.1f")
   
    with col7:
        rdw_sd = st.number_input("Распределение эритроцитов по объему, стандартное отклонение (RDW-SD):", value=None, min_value=0.0, max_value=1000.0, step=0.1, format="%.1f")
        rdw_cv = st.number_input("Распределение эритроцитов по объему, коеффициент вариации (RDW-CV):", value=None, min_value=0.0, max_value=1000.0, step=0.1, format="%.1f")
        color_index = st.number_input("Цветовой индекс (CI):", value=None, min_value=0.0, max_value=1000.0, step=0.1, format="%.1f")
        esr_westergen = st.number_input("СОЭ:", value=None, min_value=0.0, max_value=1000.0, step=0.1, format="%.1f")
    
    with col8:
        ly_rel = st.number_input("Лимфоциты, относительное количество % (LY%):", value=None, min_value=0.0, max_value=1000.0, step=0.1, format="%.1f")
        mo_rel = st.number_input("Моноциты, относительное количество % (MO%):", value=None, min_value=0.0, max_value=1000.0, step=0.1, format="%.1f")
        ne_rel = st.number_input("Нейтрофилы, относительное количество % (NE%):", value=None, min_value=0.0, max_value=1000.0, step=0.1, format="%.1f")
        eo_rel = st.number_input("Эозинофилы, относительное количество % (EO%):", value=None, min_value=0.0, max_value=1000.0, step=0.1, format="%.1f")
        ba_rel = st.number_input("Базофилы., относительное количество % (BA%):", value=None, min_value=0.0, max_value=1000.0, step=0.1, format="%.1f")

#Лейкоцитарная формула
    st.markdown(
        """
        <div class="personal-info">
        <style>.personal-info {
            background-color: #ffffff;
            padding: 20px 10px;
            font-size: 14px;
                    color: #15aabf;
            text-align: center
        }</style>
        <h3> Лейкоцитарная формула </h3>
        </div>
        """,
        unsafe_allow_html=True,
    )

    #Формы для ввода параметров лейкоцитарной формулы
    col9, col10, col11 = st.columns([1, 1, 1])
    with col9:
        ly_leico = st.number_input("Лимфоциты # (LY#):", value=None, min_value=0.0, max_value=1000.0, step=0.1, format="%.1f")
        mo_leico = st.number_input("Моноциты # (MO#):", value=None, min_value=0.0, max_value=1000.0, step=0.1, format="%.1f")

    with col10:
        esr_westergen = st.number_input("ESR_WESTERGEN", value=None, min_value=0.0, max_value=1000.0, step=0.1, format="%.1f")
        band_neut = st.number_input("Палочкоядерные нейтрофилы:", value=None, min_value=0.0, max_value=1000.0, step=0.1, format="%.1f")
        segm_neut = st.number_input("Сегментоядерные нейтрофилы:", value=None, min_value=0.0, max_value=1000.0, step=0.1, format="%.1f")
    
    with col11:
        eo_leico = st.number_input("Эозинофилы # (EO#):", value=None, min_value=0.0, max_value=1000.0, step=0.1, format="%.1f")
        ba_leico = st.number_input("Базофилы # (BA#):", value=None, min_value=0.0, max_value=1000.0, step=0.1, format="%.1f")

#Кнопка для расчета и вывода результатов с ограничением заполнения обязательных полей
    col12, col13, col14 = st.columns([1, 1, 1])

    with col13:
        if st.form_submit_button(label="Отправить"):
            required_fields = [
                gender, date_of_birth, height, weight, mcv, mch, mchc,
                ly_abs, mo_abs, ne_abs, eo_abs, ba_abs
                ]
            if any(field is None for field in required_fields):
                st.error("Пожалуйста, заполните все обязательные поля!")
            else:
                required_fields.extend([wbs, rbs, hgb, hct, plt, pct, mpv, pdw, rdw, rdw_sd, rdw_cv, ly_rel, mo_rel, ne_rel, eo_rel,
                                             ba_rel, color_index, band_neut, segm_neut, ly_leico, mo_leico, eo_leico, ba_leico, esr_westergen]),
                df = pd.DataFrame([required_fields],columns=['Sex', 'date_of_birth', 'Height', 'Weight',
        'MCV', 'MCH', 'MCHC', 'LY_ABS', 'MO_ABS', 'NE_ABS', 'EO_ABS', 'BA_ABS',
        'WBC', 'RBC', 'HGB', 'HCT', 'PLT', 'PCT', 'MPV',  'PDW', 'RDW', 'RDW_SD', 'RDW_CV', 'LY_REL', 'MO_REL', 'NE_REL', 'EO_REL',
        'BA_REL', 'COLOR_INDEX',  'BAND_NEUT',
        'SEGM_NEUT', 'LY_LEICO', 'MO_LEICO', 'EO_LEICO', 'BA_LEICO', 'ESR_Westergren'
        ])
                with get_database_session() as session:
                    df.to_sql("gbd_ng", conn, if_exists="append", index=False)
                    res = conn.execute('SELECT max(id) FROM gbd_ng')
                    session.commit()
                for row in res:
                    last_id = int(str(row[0]))
                st.session_state['user_form_id'] = last_id
                st.success("Форма успешно отправлена!")
                st.switch_page("pages/3_result.py")

