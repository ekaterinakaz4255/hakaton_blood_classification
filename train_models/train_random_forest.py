import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import pickle
import json
from tqdm import tqdm
from norms import *

# Пути к данным и сохранению моделей
input_data_path = "data/train_preprocessed.csv"
model_output_path = "models/random_forest.pkl"
icd10_mapping_path = "data/icd10_mapping.json"

# Функция для проверки отклонений от норм
def check_norms(row):
    """
    Проверяет отклонения от нормы для заданной строки данных.
    Возвращает словарь с отклонениями.
    """
    age = row["Age"]
    gender = row["Sex"]
    out_of_norm = {}
    
    norms_functions = {
        "HGB": get_hgb_norm,
        "HCT": get_hct_norm,
        "MCV": get_mcv_norm,
        "MPV": get_mpv_norm,
        "MCH": get_mch_norm,
        "MCHC": get_mchc_norm,
        "RBC": get_rbc_norm,
        "PLT": get_plt_norm,
        "WBC": get_wbc_norm,
        "PCT": get_pct_norm,
        "LY_REL": get_ly_rel_norm,
        "LY_ABS": get_ly_abs_norm,
        "NE_REL": get_ne_rel_norm,
        "NE_ABS": get_ne_abs_norm,
        "MO_REL": get_mo_rel_norm,
        "MO_ABS": get_mo_abs_norm,
        "EO_REL": get_eo_rel_norm,
        "EO_ABS": get_eo_abs_norm,
        "BA_REL": get_ba_rel_norm,
        "BA_ABS": get_ba_abs_norm,
        "BAND_NEUT": get_band_neut_norm,
        "SEGM_NEUT": get_segm_neut_norm,
        "LY_LEICO": get_ly_leico_norm,
        "MO_LEICO": get_mo_leico_norm,
        "EO_LEICO": get_eo_leico_norm,
        "BA_LEICO": get_ba_leico_norm,
        "ESR_Westergren": get_esr_norm,
        "RDW": get_rdw_norm,
        "RDW_SD": get_rdw_sd_norm,
        "RDW_CV": get_rdw_cv_norm,
        "PDW": get_pdw_norm,
    }

    for param, get_norm_fn in norms_functions.items():
        if param in row:
            try:
                if get_norm_fn.__code__.co_argcount == 2:
                    norm = get_norm_fn(age, gender)
                elif get_norm_fn.__code__.co_argcount == 1:
                    norm = get_norm_fn(age)
                else:
                    norm = get_norm_fn()
                
                lower, upper = map(float, norm.split(":"))
                value = row[param]
                if not (lower <= value <= upper):
                    out_of_norm[param] = f"{value} (норма: {norm})"
            except Exception as e:
                print(f"Ошибка при проверке нормы для {param}: {e}")
    return out_of_norm

# 1. Загрузка данных
print("Загрузка данных...")
data = pd.read_csv(input_data_path)

# 2. Кодирование целевой переменной
print("Кодирование целевой переменной...")
target_mapping = {label: idx for idx, label in enumerate(data["ICD-10"].unique())}
data["ICD-10"] = data["ICD-10"].map(target_mapping)

# Сохранение маппинга
print(f"Сохранение маппинга ICD-10 в {icd10_mapping_path}...")
with open(icd10_mapping_path, "w") as f:
    json.dump(target_mapping, f)

# 3. Разделение данных
print("Разделение данных на train и test...")
X = data.drop(columns=["ICD-10"])
y = data["ICD-10"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 4. Обучение модели RandomForestClassifier с прогрессом
print("Обучение модели RandomForestClassifier...")
model = RandomForestClassifier(random_state=42, n_estimators=100)
with tqdm(total=100, desc="Обучение модели", unit="step") as pbar:
    model.fit(X_train, y_train)
    pbar.update(100)

# 5. Оценка модели
print("Оценка модели...")
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Точность модели: {accuracy:.2f}")

print("Отчёт по классификации:")
print(classification_report(y_test, y_pred))

# 6. Сохранение модели
print(f"Сохранение модели в {model_output_path}...")
with open(model_output_path, "wb") as f:
    pickle.dump(model, f)

# 7. Проверка норм для тестовой выборки
print("Проверка норм для тестовой выборки...")
out_of_norm_results = []

for index, row in tqdm(X_test.iterrows(), total=len(X_test), desc="Проверка норм"):
    out_of_norm = check_norms(row)
    if out_of_norm:
        out_of_norm_results.append({"index": index, "out_of_norm": out_of_norm})

# Если хотите сохранить отклонения в файл
if out_of_norm_results:
    print("Сохранение отклонений в файл...")
    with open("data/out_of_norm_results_random_forest.json", "w") as f:
        json.dump(out_of_norm_results, f, indent=4)
    print("Отклонения сохранены в data/out_of_norm_results_random_forest.json")

# 8. Сохранение предсказаний
X_test_cleaned = X_test.copy()
X_test_cleaned["Predicted ICD-10"] = y_pred
X_test_cleaned.to_csv("data/test_with_predictions_random_forest.csv", index=False)

print("Обучение модели RandomForestClassifier завершено!")
