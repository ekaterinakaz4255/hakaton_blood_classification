import pandas as pd
import os
from datetime import datetime

def preprocess_data(input_path, output_path, mode="train"):
    """
    Выполняет препроцессинг данных для обучения или предсказания.
    
    Параметры:
    - input_path (str): Путь к файлу с исходными данными.
    - output_path (str): Путь для сохранения обработанных данных.
    - mode (str): Режим работы ("train" для обучения, "predict" для новых данных).
    """
    # Колонки, которые должны остаться после препроцессинга
    allowed_columns = [
        "Sex", "Age", "WBC", "RBC", "HGB", "HCT", "MCV", "MCH", "MCHC", "PLT", 
        "NE_REL", "LY_REL", "NE_ABS", "LY_ABS", "RDW_CV", "RDW_SD", "RDW", "PCT", 
        "MPV", "PDW", "MO_REL", "EO_REL", "BA_REL", "MO_ABS", "EO_ABS", "BA_ABS", 
        "COLOR_INDEX", "ESR_Westergren", "BAND_NEUT", "SEGM_NEUT", "EO_LEICO", 
        "LY_LEICO", "MO_LEICO", "BA_LEICO", "ICD-10"
    ]

    def calculate_age(df):
        """
        Рассчитать возраст (Age) на основе даты рождения.
        """
        date_columns = [col for col in df.columns if "date" in col.lower()]
        if date_columns:
            dob_col = date_columns[0]  # Берём первую найденную колонку с датой
            try:
                current_date = datetime.now()
                df["Age"] = df[dob_col].apply(
                    lambda x: (current_date - pd.to_datetime(x)).days // 365 if pd.notnull(x) else None
                )
            except Exception as e:
                print(f"Ошибка при обработке даты рождения: {e}")
        if "Age" not in df.columns:
            df["Age"] = None  # Если Age так и не удалось рассчитать, добавляем колонку с пустыми значениями
        return df

    # Проверка наличия файла
    if not os.path.exists(input_path):
        print(f"Файл {input_path} не найден. Прекращение работы.")
        return

    # Загрузка данных
    print(f"Загрузка данных из {input_path}...")
    data = pd.read_csv(input_path)

    # Препроцессинг: добавление возраста
    if "Age" not in data.columns:
        data = calculate_age(data)

    # Фильтрация колонок
    missing_columns = [col for col in allowed_columns if col not in data.columns]
    if missing_columns:
        print(f"Предупреждение: следующие колонки отсутствуют в данных и будут пропущены: {missing_columns}")
    data = data[[col for col in allowed_columns if col in data.columns]]

    # Обработка пропущенных значений
    print("Обработка пропущенных значений...")
    for col in data.columns:
        if data[col].dtype in ["float64", "int64"]:  # Числовые колонки
            data[col] = data[col].fillna(0)  # Заполнение нулями
        elif data[col].dtype == "object":  # Категориальные колонки
            data[col] = data[col].fillna("Unknown")  # Заполнение строкой "Unknown"

    # Проверка целевой переменной в режиме обучения
    if mode == "train" and "ICD-10" not in data.columns:
        raise ValueError("В режиме обучения колонка 'ICD-10' обязательна.")

    # Закрепление списка диагнозов
    if mode == "train" and "ICD-10" in data.columns:
        diagnoses = data["ICD-10"].unique()
        diagnoses_path = "data/diagnoses.txt"
        print(f"Сохранение списка диагнозов в {diagnoses_path}...")
        with open(diagnoses_path, "w") as f:
            f.writelines("\n".join(diagnoses))

    # Сохранение обработанных данных
    print(f"Сохранение обработанных данных в {output_path}...")
    data.to_csv(output_path, index=False)
    print("Препроцессинг завершён.")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Скрипт для препроцессинга данных")
    parser.add_argument("--input", required=True, help="Путь к входному CSV файлу")
    parser.add_argument("--output", required=True, help="Путь для сохранения обработанных данных")
    parser.add_argument("--mode", choices=["train", "predict"], default="train", help="Режим работы: 'train' или 'predict'")
    args = parser.parse_args()

    preprocess_data(input_path=args.input, output_path=args.output, mode=args.mode)
