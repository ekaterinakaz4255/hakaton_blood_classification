import os
import pickle
import pandas as pd
from collections import Counter
from tqdm import tqdm
import json
from norms import check_norms

# Пути к моделям и данным
models_dir = "models/"
input_data_path = "data/preprocessed_data.csv"
output_predictions_path = "data/ensemble_predictions.csv"
icd10_mapping_path = "data/icd10_mapping.json"


# 1. Загрузка моделей
def load_models(models_dir):
    models = []
    for file in os.listdir(models_dir):
        if file.endswith(".pkl"):
            with open(os.path.join(models_dir, file), "rb") as f:
                model = pickle.load(f)
                models.append(model)
    return models

# 2. Загрузка данных
def load_data(input_data_path=None):
    if input_data_path and os.path.exists(input_data_path):
        print(f"Загрузка данных из базы данных {input_data_path}...")
        data = pd.read_csv(input_data_path)
        return data
    else:
        raise FileNotFoundError("Не удалось найти данные")

# 3. Проверка соответствия признаков
def validate_features(data, model_features):
    data_features = set(data.columns)
    model_features = set(model_features)
    missing_features = model_features - data_features
    extra_features = data_features - model_features
    return missing_features, extra_features

# 4. Реализация голосования
def ensemble_predict(models, X):
    predictions = []
    for model in tqdm(models, desc="Получение предсказаний от моделей"):
        predictions.append(model.predict(X))
    
    # Голосование (majority vote)
    final_predictions = []
    for preds in zip(*predictions):
        vote_count = Counter(preds)
        final_predictions.append(vote_count.most_common(1)[0][0])
    
    return final_predictions

# 5. Генерация текстового сообщения
def generate_text_message(predictions, mapping, X):
    message = []
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
    return "\n".join(message)


# 6. Функция для обработки пациента
def generate_recommendation(patient_text):
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

    # Генерация рекомендации
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

    return recommendation


# Основной скрипт
if __name__ == "__main__":
    print("Загрузка моделей...")
    models = load_models(models_dir)
    
    print("Загрузка данных...")
    data = load_data(input_data_path=input_data_path)

    print("Загрузка маппинга ICD-10...")
    with open(icd10_mapping_path, "r") as f:
        icd10_mapping = json.load(f)
    
    print("Предсказание ансамбля моделей...")
    predictions = ensemble_predict(models, data)
    
    print("Сохранение предсказаний...")
    data["Predicted ICD-10"] = predictions
    data.to_csv(output_predictions_path, index=False)
    
    print("Генерация текстового сообщения...")
    patient_text = generate_text_message(predictions, icd10_mapping, data)
    
    print("Генерация рекомендаций...")
    recommendation = generate_recommendation(patient_text)
    
    print("Работа завершена. Результаты сохранены.")