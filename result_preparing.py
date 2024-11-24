import sqlite3
import pandas as pd
import pickle
import numpy as np
from datetime import datetime

# Подключаемся к базе данных
conn = sqlite3.connect('data/gbd.db')

# Выполняем запрос к базе данных
cursor = conn.cursor()

# Получаем имена таблиц
table_list = [a for a in cursor.execute("SELECT name FROM sqlite_master WHERE type = 'table'")]

# Берем данные из таблицы
cursor.execute(f'SELECT * FROM {table_list[0][0]}') 

# Получаем данные из базы данных
data = cursor.fetchall()

# Достаем названия столбцов
names = list(map(lambda x: x[0], cursor.description))

# Закрываем подключение к базе данных
conn.close()

# Создаем датафрейм из данных
df = pd.DataFrame(data, columns=names)

# Кодируем столбец 'Пол'
df['gender'] = df['gender'].map({'Женский': 0, 'Мужской': 1})

# Функция для вычисления количества полных лет
def calculate_age(birthdate):
    today = datetime.today()
    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    return age

# Преобразуем столбец "Дата рождения" в формат datetime
df['date_of_birth'] = pd.to_datetime(df['date_of_birth'], format='%Y-%m-%d')

# Вычисляем возраст и добавляем новый столбец
df['age'] = df['date_of_birth'].apply(calculate_age)
df.drop(columns=['date_of_birth'], axis=1, inplace=True)

# Сохраняем датафрейм в файл CSV
df.to_csv('data/income_data.csv', index=False)

# Читаем файл с сериализованной моделью
with open('myfile.pkl', 'rb') as pkl_file:
    model = pickle.load(pkl_file)

# Получаем предсказание
prediction = model.predict(np.array(df).reshape(1, -1))

# Обработка prediction в соответствующий формат