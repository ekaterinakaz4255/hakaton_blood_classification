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
    background-size: cover;
    background-position: center center;
    background-repeat: repeat;
    background-image: url("data:image/svg+xml;utf8,%3Csvg width=%222000%22 height=%221400%22 xmlns=%22http:%2F%2Fwww.w3.org%2F2000%2Fsvg%22%3E%3Cstyle%3E.shadow_right{-webkit-filter:drop-shadow(-5px -5px 15px %23b6dae0);filter:drop-shadow(-5px -5px 15px %23b6dae0)}.shadow_left{-webkit-filter:drop-shadow(5px 5px 15px %23b6dae0);filter:drop-shadow(5px 5px 15px %23b6dae0)}%3C%2Fstyle%3E%3Cdefs%3E%3ClinearGradient id=%22gradient__0%22 x1=%220%22 y1=%220%22 x2=%220%22 y2=%221%22%3E%3Cstop stop-color=%22%23b6dae0%22 offset=%220%25%22%2F%3E%3Cstop stop-color=%22%23fff%22 offset=%2225%25%22%2F%3E%3Cstop stop-color=%22%23fff%22 offset=%2250%25%22%2F%3E%3Cstop stop-color=%22%23fff%22 offset=%2275%25%22%2F%3E%3Cstop stop-color=%22%23b6dae0%22 offset=%22100%25%22%2F%3E%3C%2FlinearGradient%3E%3Cfilter id=%22grain%22 x=%22-1000%22 y=%22-700%22 width=%224000%22 height=%222800%22 filterUnits=%22userSpaceOnUse%22%3E&gt;%3CfeFlood flood-color=%22%23fff%22 result=%22neutral-gray%22%2F%3E%3CfeTurbulence type=%22fractalNoise%22 baseFrequency=%222.5%22 numOctaves=%22100%22 stitchTiles=%22stitch%22 result=%22noise%22%2F%3E%3CfeColorMatrix in=%22noise%22 type=%22saturate%22 values=%220%22 result=%22destaturatedNoise%22%2F%3E%3CfeComponentTransfer in=%22desaturatedNoise%22 result=%22theNoise%22%3E%3CfeFuncA type=%22table%22 tableValues=%220 0 0.4 0%22%2F%3E%3C%2FfeComponentTransfer%3E%3CfeBlend in=%22SourceGraphic%22 in2=%22theNoise%22 mode=%22soft-light%22 result=%22noisy-image%22%2F%3E%3C%2Ffilter%3E%3C%2Fdefs%3E%3Cg filter=%22url(%23grain)%22%3E%3Cpath fill=%22%23b6dae0%22 d=%22M0 0h2000v1400H0z%22%2F%3E%3Cpath id=%22rect__4%22 fill=%22url(%23gradient__0)%22 d=%22M888.889 311.111h222.222v777.778H888.889z%22%2F%3E%3Cpath class=%22shadow_left%22 id=%22rect__5%22 fill=%22url(%23gradient__0)%22 d=%22M1111.111 233.333h222.222v933.333h-222.222z%22%2F%3E%3Cpath class=%22shadow_left%22 id=%22rect__6%22 fill=%22url(%23gradient__0)%22 d=%22M1333.333 155.556h222.222v1088.889h-222.222z%22%2F%3E%3Cpath class=%22shadow_left%22 id=%22rect__7%22 fill=%22url(%23gradient__0)%22 d=%22M1555.556 77.778h222.222v1244.444h-222.222z%22%2F%3E%3Cpath class=%22shadow_left%22 id=%22rect__8%22 fill=%22url(%23gradient__0)%22 d=%22M1777.778 0H2000v1400h-222.222z%22%2F%3E%3Cpath class=%22shadow_right%22 id=%22rect__3%22 fill=%22url(%23gradient__0)%22 d=%22M666.667 233.333h222.222v933.333H666.667z%22%2F%3E%3Cpath class=%22shadow_right%22 id=%22rect__2%22 fill=%22url(%23gradient__0)%22 d=%22M444.444 155.556h222.222v1088.889H444.444z%22%2F%3E%3Cpath class=%22shadow_right%22 id=%22rect__1%22 fill=%22url(%23gradient__0)%22 d=%22M222.222 77.778h222.222v1244.444H222.222z%22%2F%3E%3Cpath class=%22shadow_right%22 id=%22rect__0%22 fill=%22url(%23gradient__0)%22 d=%22M0 0h222.222v1400H0z%22%2F%3E%3C%2Fg%3E%3C%2Fsvg%3E");
}
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