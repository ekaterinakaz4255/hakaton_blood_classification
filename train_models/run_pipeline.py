import os
import sys

# Пути к скриптам
preprocess_script = "./preprocess.py"
ensemble_script = "./ensemble_predict.py"

# Пути к данным
input_file = "data/new_data.csv"  # Входной файл с новыми данными
output_file = "data/new_data_preprocessed.csv"  # Выходной файл для обработанных данных

# Функция проверки существования файла
def check_file_exists(file_path):
    if not os.path.exists(file_path):
        print(f"Ошибка: Файл '{file_path}' не найден.")
        sys.exit(1)

# Проверка наличия входного файла
check_file_exists(input_file)

# 1. Запуск preprocess.py
print("Шаг 1: Обработка данных через preprocess.py...")
preprocess_command = f"python {preprocess_script} --input {input_file} --output {output_file} --mode predict"
if os.system(preprocess_command) != 0:
    print("Ошибка при запуске preprocess.py. Проверьте входные данные.")
    sys.exit(1)

# Проверка наличия обработанных данных
check_file_exists(output_file)

# 2. Запуск ensemble_predict.py
print("Шаг 2: Запуск ансамбля через ensemble_predict.py...")
ensemble_command = f"python {ensemble_script}"
if os.system(ensemble_command) != 0:
    print("Ошибка при запуске ensemble_predict.py. Проверьте модели и предобработанные данные.")
    sys.exit(1)

print("Пайплайн завершён успешно!")


