import sqlite3
import pandas as pd
import pickle
import numpy as np
from datetime import datetime
import os

# Путь к файлу базы данных
db_path = 'data/gbd.db'

# Проверяем существование файла в директории
if not os.path.exists(db_path):
    raise FileNotFoundError(f"Файл '{db_path}' не существует.")

# Подключаемся к базе данных
conn = sqlite3.connect(db_path)

# Выполняем запрос к базе данных
cursor = conn.cursor()

# Берем только последнюю строку из таблицы
cursor.execute(f'SELECT * FROM gbd_ng ORDER BY rowid DESC LIMIT 1') 

# Получаем данные из базы данных
data = cursor.fetchall()

# Достаем названия столбцов
names = list(map(lambda x: x[0], cursor.description))

# Закрываем подключение к базе данных
conn.close()

# Создаем датафрейм из данных
df = pd.DataFrame(data, columns=names)

print('Данные успешно загружены, начинаем обработку...')

# Кодируем столбец 'Пол'
try:
    df['gender'] = df['gender'].map({'Женский': 0, 'Мужской': 1})
    if df['gender'].isnull().any():
        raise ValueError('Недопустимое значение: Nan в столбце "Пол"')
except Exception as e:
                print(f"Ошибка при кодировании пола: {e}")

# Функция для вычисления количества полных лет
def calculate_age(birthdate):
    today = datetime.today()
    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    return age

# Расчет возраста 
try: 
    # Преобразуем столбец "Дата рождения" в формат datetime
    df['date_of_birth'] = pd.to_datetime(df['date_of_birth'], format='%Y-%m-%d')
    # Вычисляем возраст и добавляем новый столбец
    df['age'] = df['date_of_birth'].apply(calculate_age)
    df.drop(columns=['date_of_birth'], axis=1, inplace=True)
    if df['age'].isnull().any():
        raise ValueError('Недопустимое значение: Nan в столбце "Возраст"')
except Exception as e:
                print(f"Ошибка при расчете возраста: {e}")

# Обработка пропусков 

# Колонки, которые должны остаться после препроцессинга
allowed_columns = [
        "Sex", "Age", "WBC", "RBC", "HGB", "HCT", "MCV", "MCH", "MCHC", "PLT", 
        "NE_REL", "LY_REL", "NE_ABS", "LY_ABS", "RDW_CV", "RDW_SD", "RDW", "PCT", 
        "MPV", "PDW", "MO_REL", "EO_REL", "BA_REL", "MO_ABS", "EO_ABS", "BA_ABS", 
        "COLOR_INDEX", "ESR_Westergren", "BAND_NEUT", "SEGM_NEUT", "EO_LEICO", 
        "LY_LEICO", "MO_LEICO", "BA_LEICO", "ICD-10"
    ]

 # Фильтрация колонок
missing_columns = [col for col in allowed_columns if col not in df.columns]
if missing_columns:
    print(f"Предупреждение: следующие колонки отсутствуют в данных и будут пропущены: {missing_columns}")
df = df[[col for col in allowed_columns if col in df.columns]]

# Обработка пропущенных значений
for col in df.columns:
    if df[col].dtype in ["float64", "int64"]:  # Числовые колонки
        df[col] = df[col].fillna(0)  # Заполнение нулями
    elif df[col].dtype == "object":  # Категориальные колонки
        df[col] = df[col].fillna("Unknown")  # Заполнение строкой "Unknown"

print('Данные обработаны, сохраняем в папку data...')

# Сохраняем датафрейм в файл CSV
df.to_csv('data/income_data.csv', index=False)

print('Данные успешно сохранены, переходим к обучению моделей...')

# Читаем файл с сериализованной моделью
with open('myfile.pkl', 'rb') as pkl_file:
    model = pickle.load(pkl_file)

# Получаем предсказание
prediction = model.predict(np.array(df).reshape(1, -1))

print('Предсказание получено, формируем заключение...')

# Обработка prediction в соответствующий формат