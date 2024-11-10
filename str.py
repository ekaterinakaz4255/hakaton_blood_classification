import streamlit as st
import time
import datetime


st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

st.image('title_img.png', width=400)
#Заголовок приложения
st.title("Распознование результатов общего анализа крови")
st.write("## Команда №2.👋")
st.markdown(
    """
    ## Состав команды
    **Тимлид команды**: 
    
    Казаченко Екатерина
    
    **Члены команды**:
    - Борковская Евгения
    - Бондарева Алина
    - Хван Ок Хи

    ## Цель хакатона:

    Разработать сервис, который на основе данных общего анализа крови проводит диагностику и выдает рекомендацию обратится к определенному врачу (или нет) с указанием срочности.

"""
)

#Поля ввода личной информации (пол, возраст, рост и вес (2 последних опционально))
st.title("Заполните форму")

# Создаем форму с текстовыми полями
with st.form("form"):
    #Личная информация пациента
    st.title("Личная информация")
    option = st.selectbox("Выберите пол:", ["Мужской", "Женский"])
    date_input = st.date_input("Выберите дату:", min_value=datetime.date(1900, 1, 1), max_value=datetime.date.today())
    
    #Параметры ОАК
    st.title('Параметры общего анализа крови')
    # Кнопка для отправки формы
    submit = st.form_submit_button("Отправить")
    
    # Выводим сообщение, когда форма отправлена
    if submit:
        st.write(f"Результаты скоро будут готовы, подождите немного")


# Пример использования фрагмента с автообновлением
st.title("Пример с фрагментом")

@st.experimental_fragment(run_every="10s")
def fragment():
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.write(f"Текущее время: {current_time}")
    st.button("Перезапустить фрагмент вручную")

# Запуск фрагмента
fragment()
