import sqlite3
import os
import pandas as pd
import numpy as np
from datetime import datetime
import sys
import pickle
import json
from collections import Counter
from norms import check_norms

models_dir = "models/"
icd10_mapping_path = "data/icd10_mapping.json"

# Функция для загрузки моделей
def load_models(models_dir):
    models = []
    try:
        for file in os.listdir(models_dir):
            if file.endswith(".pkl"):
                with open(os.path.join(models_dir, file), "rb") as f:
                    model = pickle.load(f)
                    models.append(model)
    except Exception as e:
        print(f"Error loading models: {e}")
    return models

# Функция для расчета возраста на основе даты рождения
def calculate_age(df):
    current_date = datetime.now()
    try:
        df['Age'] = df['Age'].apply(
            lambda x: (current_date - pd.to_datetime(x)).days // 365 if pd.notnull(x) else None
        )
        df['Age'].fillna(0, inplace=True)
    except Exception as e:
        print(f"Error calculating age: {e}")
    return df

# Функция для реализации голосования
def ensemble_predict(models, X):
    X = X.drop(columns=["Height", "Weight"])
    predictions = []
    try:
        for model in models:
            predictions.append(model.predict(X))
    except Exception as e:
        print(f"Error making predictions: {e}")
        
    # Голосование (majority vote)
    final_predictions = []
    try:
        for preds in zip(*predictions):
            vote_count = Counter(preds)
            final_predictions.append(vote_count.most_common(1)[0][0])
    except Exception as e:
        print(f"Error voting: {e}")
    return final_predictions

# Функция для генерации текстового сообщения
def generate_text_message(predictions, mapping, X):
    message = []
    
    try:
        for idx, pred in enumerate(predictions):
            # Определяем диагноз
            diagnosis = [k for k, v in mapping.items() if v == pred][0]
            
            # Получаем данные пациента
            patient_data = X.iloc[idx].to_dict()
            age = patient_data.get("Age", "не указан")
            gender = "Мужской" if patient_data.get("Sex") == 1 else "Женский"
            weight = patient_data.get("Weight", None)
            height = patient_data.get("Height", None)
            
            # Рассчитываем BMI, если есть данные о весе и росте
            bmi_message = ""
            if weight and height:
                try:
                    height_m = height / 100  # Преобразуем рост в метры
                    bmi = weight / (height_m ** 2)
                    if bmi < 16:
                        bmi_category = "Значительный дефицит массы тела"
                    elif 16 <= bmi < 18.5:
                        bmi_category = "Дефицит массы тела"
                    elif 18.5 <= bmi < 25:
                        bmi_category = "Норма"
                    elif 25 <= bmi < 30:
                        bmi_category = "Лишний вес"
                    elif 30 <= bmi < 35:
                        bmi_category = "Ожирение первой степени"
                    elif 35 <= bmi < 40:
                        bmi_category = "Ожирение второй степени"
                    else:
                        bmi_category = "Ожирение третьей степени"
                    bmi_message = f"  - Индекс массы тела (BMI): {bmi:.2f} ({bmi_category}).\n"
                except Exception as e:
                    bmi_message = "  - Не удалось рассчитать BMI из-за ошибки.\n"

            # Проверяем отклонения от норм
            out_of_norm = check_norms(patient_data)
            
            # Формируем сообщение
            patient_message = f"Пациент {idx + 1} (Возраст: {age}, Пол: {gender}):\n"
            patient_message += f"  - Диагноз: {diagnosis}.\n"
            if bmi_message:
                patient_message += bmi_message
            
            if out_of_norm:
                patient_message += "  - Отклонения от нормы:\n"
                for param, info in out_of_norm.items():
                    if isinstance(info, dict):  # Проверяем, что info — это словарь
                        value = info.get('value', 'N/A')
                        norm = info.get('norm', 'N/A')
                        patient_message += f"    * {param}: значение {value} (норма {norm})\n"
                    else:
                        patient_message += f"    * {param}: {info}\n"
            else:
                patient_message += "  - Все показатели в норме.\n"
            
            message.append(patient_message)
    except Exception as e:
        print(f"Error generating text message: {e}")    
           
    return "\n".join(message)

# Функция для обработки рекомендации для пользователя
def generate_recommendation(patient_text):
    try: 
        lines = patient_text.strip().split("\n")
        # Извлекаем возраст
        age_line = next((line for line in lines if "Возраст:" in line), None)
        age = float(age_line.split(":")[1].split(",")[0]) if age_line else None

        # Извлекаем диагноз
        diagnosis_line = next((line for line in lines if "Диагноз:" in line), None)
        if diagnosis_line:
            diagnosis = diagnosis_line.split(":")[1].strip()
        else:
            diagnosis = "неизвестно"

        # Проверка на отклонения
        deviations = any("*" in line for line in lines if "Отклонения от нормы:" in line or "    *" in line)

    except Exception as e:
        print(f"Error generating recommendation (1): {e}")
        
    # Генерация рекомендации
    try:
        if diagnosis.lower() == "норма.":
            if deviations:
                recommendation = (
                    "Акулье одобрение! Но для более бодрого плавания по жизни рекомендую заглянуть к врачу на плановый осмотр! "
                    "Учтите отклонения в ваших анализах, чтобы оставаться здоровым!"
                )
            else:
                recommendation = (
                    "Акулье одобрение! Но для более бодрого плавания по жизни рекомендую заглянуть к врачу на плановый осмотр!"
                )
        elif age is not None and age < 18:  # Проверка на возраст
            recommendation = (
                "Не медли и подплывай к педиатру! Пусть проверит твои показатели и, если будет необходимо, направит к более узкому специалисту!"
            )
        else:
            recommendation = (
                "Ой-ой, вижу тут отклонения от норм показателей, а это значит, что тебе нужно посетить врача! Обратись скорее к своему терапевту, чтобы узнать, как исправить свое здоровье!"
            )
    except Exception as e:
        print(f"Error generating recommendation (2): {e}")

    return recommendation

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
    print('Проверка соответствия длины row и количества колонок...')
    if (len(row) - 1) != len(ordered_columns):
        raise ValueError("Number of elements in row does not match number of columns")
    print('Преобразование row в DataFrame...')
    row_n = row[1:]
    df = pd.DataFrame([row_n], columns=ordered_columns)
    #df.set_index('id', inplace=True)
    
    # 2) Расчет возраста по дате рождения
    print("Расчет возраста по дате рождения...")
    try:
        df = calculate_age(df)
    except Exception as e:
        print(f"Error calculating age: {e}")

    # 3) Преобразование пола в числовое значение
    print("Преобразование пола в числовое значение...")
    try:
        df['Sex'] = df['Sex'].apply(lambda x: 1 if x == 'Мужской' else 0)
    except Exception as e:
        print(f"Error converting sex: {e}")

    # 4) Обработка пропусков
    print("Обработка пропусков...")
    df.fillna(0, inplace=True)
      
    # 5) Загрузка моделей и осуществление предсказания ансамблем
    print("Загрузка моделей...")
    models = load_models(models_dir)
    
    print("Загрузка маппинга ICD-10...")
    with open(icd10_mapping_path, "r") as f:
        icd10_mapping = json.load(f)
        
    print("Предсказание ансамбля моделей...")
    predictions = ensemble_predict(models, df)  
    
    # 6) Генерация текстового сообщения и формирование рекомендации для пользователя
    print("Генерация текстового сообщения...")
    patient_text = generate_text_message(predictions, icd10_mapping, df)
    
    print("Генерация рекомендаций...")
    recommendation = generate_recommendation(patient_text)
    
    print("Предсказание получено и передано дальше...")
    return recommendation

# функция классификации
def diagnosis_classifier(id: int):
    # путь к базе данных
    db_path = 'database/gbd.db'
    try:
        # подключаемся к базе данных
        with sqlite3.connect(db_path) as conn:
            # делаем селект из базы данных
            cur = conn.cursor()
            cur.execute('select * from gbd_ng where id =?', (id,))
            # сохраняем результат в кортеж с именем row
            row = cur.fetchone()
            print('Данные получены из базы данных...')
    # проверяем что нет ошибки
    except sqlite3.OperationalError as e:
        print("error")

    # запускаем функцию для пайплайна предсказания и генерации заключения
    print('Запускаем функцию для пайплайна предсказания и генерации заключения...')
    return run_pipeline(row)