import sqlite3
import os
import pandas as pd
from datetime import datetime
import sys

# Функция для расчета возраста
def calculate_age(df):
    """
    Рассчитать возраст (Age) на основе даты рождения.
    """
    current_date = datetime.now()
    df['Age'] = df['Age'].apply(
        lambda x: (current_date - pd.to_datetime(x)).days // 365 if pd.notnull(x) else None
    )
    df['Age'].fillna(0, inplace=True)
    return df

# Функция для запуска пайплайна обработки данных и ансамбля для предсказания
def run_pipeline(row):
    '''
    пример row: 
    (32, 'Мужской', '2024-11-01', 123, 123, 1.0, 1.0, 1.0, 1.0, 1.0, None, None, 1.0, 1.0, 1.0, None, None, None, None, None, None, None, None, None, None, 1.0, 1.0, 1.0, 1.0, 1.0, None, None, None, None, None, None, None)
    '''
    # 1) Переводим данные (row) в DataFrame и присваиваем имена столбцов
    # Колонки в фиксированном порядке
    ordered_columns = [
        'Sex', 'Age', 'Weight', 'Height', 'WBC', 'RBC', 'HGB', 'HCT', 'PLT', 'PCT', 'MPV', 'MCV',
        'MCH', 'MCHC', 'PDW', 'RDW', 'RDW_SD', 'RDW_CV', 'LY_REL', 'MO_REL', 'NE_REL', 'EO_REL',
        'BA_REL', 'COLOR_INDEX', 'LY_ABS', 'MO_ABS', 'NE_ABS', 'EO_ABS', 'BA_ABS', 'BAND_NEUT',
        'SEGM_NEUT', 'LY_LEICO', 'MO_LEICO', 'EO_LEICO', 'BA_LEICO', 'ESR_Westergren'
    ]
    
    if (len(row) - 1) != len(ordered_columns):
        raise ValueError("Number of elements in row does not match number of columns")
    
    df = pd.DataFrame([row], columns=ordered_columns)
    df.set_index('id', inplace=True)

    # 2) Расчет возраста по дате рождения
    try:
        df = calculate_age(df)
    except Exception as e:
        print(f"Error calculating age: {e}")

    # 3) Преобразование пола в числовое значение
    try:
        df['Sex'] = df['Sex'].apply(lambda x: 1 if x == 'Мужской' else 0)
    except Exception as e:
        print(f"Error converting sex: {e}")

    # 4) Обработка пропусков
    df.fillna(0, inplace=True)

    # 5) Сохранение обработанных данных
    df.to_csv("data/preprocessed_data.csv", index=True)
    print("Препроцессинг входящих данных завершён успешно!")
    
    # Пути к скриптам
    ensemble_script = "ensemble_predict.py"
    
    # 6) Запуск ensemble_predict.py
    ensemble_command = f"python {ensemble_script}"
    if os.system(ensemble_command) != 0:
        print("Ошибка при запуске ensemble_predict.py")
        sys.exit(1)
    
    # Для тестирования просто возвращаем текст рекоммендации
    test_recommendation = "Текст рекоммендации успешно сгенерирован"
    
    return test_recommendation

# функция классификации
def diagnosis_classifier(id: int):
    # путь к базе данных
    db_path = 'data/gbd.db'
    try:
        # подключаемся к базе данных
        with sqlite3.connect(db_path) as conn:
            # делаем селект из базы данных
            cur = conn.cursor()
            cur.execute('select * from gbd_ng where id =?', (id,))
            # сохраняем результат в кортеж с именем row
            row = cur.fetchone()
            # проверяем что нет ошибки
    except sqlite3.OperationalError as e:
        print("error")

    # запускаем функцию для пайплайна предсказания и генерации заключения
    return run_pipeline(row)