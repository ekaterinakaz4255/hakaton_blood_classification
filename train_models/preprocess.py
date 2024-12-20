import sqlite3
import pandas as pd
from datetime import datetime
import os

def preprocess_data(input_path=None, db_path=None, output_path=None, mode="train"):
    """
    Выполняет препроцессинг данных для обучения или предсказания.

    Параметры:
    - input_path (str): Путь к файлу с исходными данными (если не указан db_path).
    - db_path (str): Путь к базе данных SQLite (если не указан input_path).
    - output_path (str): Путь для сохранения обработанных данных. Если не указан, автоматически добавляется `_preprocessed`.
    - mode (str): Режим работы ("train" для обучения, "predict" для новых данных).
    """
    # Колонки в фиксированном порядке
    ordered_columns = [
        'Sex', 'Age', 'Weight', 'Height', 'WBC', 'RBC', 'HGB', 'HCT', 'PLT', 'PCT', 'MPV', 'MCV',
        'MCH', 'MCHC', 'PDW', 'RDW', 'RDW_SD', 'RDW_CV', 'LY_REL', 'MO_REL', 'NE_REL', 'EO_REL',
        'BA_REL', 'COLOR_INDEX', 'LY_ABS', 'MO_ABS', 'NE_ABS', 'EO_ABS', 'BA_ABS', 'BAND_NEUT',
        'SEGM_NEUT', 'LY_LEICO', 'MO_LEICO', 'EO_LEICO', 'BA_LEICO', 'ESR_Westergren', 'ICD-10'
    ]

    def calculate_age(df):
        """
        Рассчитать возраст (Age) на основе даты рождения.
        """
        date_columns = [col for col in df.columns if "date" in col.lower()]
        if date_columns:
            dob_col = date_columns[0]
            try:
                current_date = datetime.now()
                df["Age"] = df[dob_col].apply(
                    lambda x: (current_date - pd.to_datetime(x)).days // 365 if pd.notnull(x) else None
                )
            except Exception as e:
                print(f"Ошибка при обработке даты рождения: {e}")
        if "Age" not in df.columns:
            df["Age"] = None
        return df

    # Загрузка данных из SQLite или CSV
    if db_path:
        if not os.path.exists(db_path):
            raise FileNotFoundError(f"Файл базы данных '{db_path}' не найден.")
        
        print(f"Загрузка данных из базы данных {db_path}...")
        conn = sqlite3.connect(db_path)
        query = "SELECT * FROM gbd_ng ORDER BY rowid DESC LIMIT 1"
        data = pd.read_sql_query(query, conn)
        conn.close()
    elif input_path:
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"Файл {input_path} не найден.")
        
        print(f"Загрузка данных из {input_path}...")
        data = pd.read_csv(input_path)
    else:
        raise ValueError("Необходимо указать либо 'input_path', либо 'db_path'.")

    # Добавление возраста
    if "Age" not in data.columns:
        data = calculate_age(data)

    # Удаление лишних колонок и добавление недостающих
    missing_columns = [col for col in ordered_columns if col not in data.columns]
    for col in missing_columns:
        print(f"Добавление недостающей колонки: {col}")
        if col in ["Weight", "Height"]:
            data[col] = None  # Значения по умолчанию для вес/рост
        else:
            data[col] = 0  # Значения по умолчанию для остальных колонок

    # Фильтрация и сортировка колонок
    data = data[[col for col in ordered_columns if col in data.columns]]

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

    # Автоматически добавляем `_preprocessed` к названию выходного файла
    if output_path is None:
        output_path = "data/preprocessed_data.csv"

    # Сохранение обработанных данных
    print(f"Сохранение обработанных данных в {output_path}...")
    data.to_csv(output_path, index=False)
    print("Препроцессинг завершён успешно!")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Скрипт для препроцессинга данных")
    parser.add_argument("--input", required=False, help="Путь к входному CSV файлу")
    parser.add_argument("--db", required=False, help="Путь к файлу базы данных SQLite")
    parser.add_argument("--output", required=False, help="Путь для сохранения обработанных данных")
    parser.add_argument("--mode", choices=["train", "predict"], default="train", help="Режим работы: 'train' или 'predict'")
    args = parser.parse_args()

    preprocess_data(input_path=args.input, db_path=args.db, output_path=args.output, mode=args.mode)
