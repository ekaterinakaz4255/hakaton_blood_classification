import pandas as pd
import numpy as np

def get_hgb_norm(age, gender):
    """Возвращает норму гемоглобина в зависимости от возраста и пола."""
    if age < 18:
        # Норма для детей
        if age == 0:  # Возраст < 1 месяца (младенцы)
            return "152:235"
        elif 1 <= age <= 13 / 365:  # 2–13 дней
            return "150:240"
        elif 14 / 365 <= age <= 23 / 365:  # 14–23 дня
            return "127:187"
        elif 24 / 365 <= age <= 30 / 365:  # 24–30 дней
            return "103:179"
        elif age < 2 / 12:  # 1 месяц
            return "90:166"
        elif age < 3 / 12:  # 2 месяца
            return "92:150"
        elif age < 4 / 12:  # 3 месяца
            return "96:135"
        elif age < 5 / 12:  # 4 месяца
            return "96:135"
        elif age < 8 / 12:  # 5–7 месяцев
            return "101:132"
        elif age < 11 / 12:  # 8–10 месяцев
            return "105:135"
        elif age < 1:  # 11 месяцев
            return "107:131"
        elif age < 5:  # 12 месяцев — 4 года
            return "108:132"
        elif age < 10:  # 5–9 лет
            return "111:143"
        elif age < 12:  # 10–11 лет
            return "119:147"
        elif age < 15:  # 12–14 лет
            if gender == 1:  # Мальчики
                return "120:160"
            else:  # Девочки
                return "115:150"
        elif age < 18:  # 15–17 лет
            if gender == 1:  # Юноши
                return "117:166"
            else:  # Девушки
                return "117:153"
    else:
        # Норма для взрослых
        if gender == 1:  # Мужчины
            if 18 <= age <= 44:
                return "132:173"
            elif 45 <= age <= 64:
                return "131:172"
            else:  # От 65 лет
                return "126:174"
        else:  # Женщины
            if 18 <= age <= 44:
                return "117:155"
            elif 45 <= age <= 64:
                return "117:160"
            else:  # От 65 лет
                return "117:161"

def get_hct_norm(age, gender):
    """Возвращает норму гематокрита в зависимости от возраста и пола."""
    if age < 18:
        # Норма для детей
        if age == 0:  # Возраст < 1 месяца (младенцы)
            return "41:65" if age <= 13 / 365 else "33:55"
        elif age < 2 / 12:  # 2 месяца
            return "32:44"
        elif age < 6 / 12:  # 3–5 месяцев
            return "31:41"
        elif age < 9 / 12:  # 6–8 месяцев
            return "32:40"
        elif age < 12 / 12:  # 9–11 месяцев
            return "33:41"
        elif age < 3:  # 12 месяцев — 2 года
            return "32:40"
        elif age < 6:  # 3–5 лет
            return "32:42"
        elif age < 9:  # 6–8 лет
            return "33:41"
        elif age < 12:  # 9–11 лет
            return "34:43"
        else:
            # Норма для подростков
            if gender == 1:  # Мужчины
                if 12 <= age < 15:
                    return "35:45"
                elif 15 <= age < 18:
                    return "37:48"
            else:  # Женщины
                if 12 <= age < 18:
                    return "34:44"
    else:
        # Норма для взрослых
        if gender == 1:  # Мужчины
            if 18 <= age <= 44:
                return "39:49"
            elif 45 <= age <= 64:
                return "39:50"
            else:  # От 65 лет
                return "37:51"
        else:  # Женщины
            if 18 <= age <= 44:
                return "35:45"
            else:  # От 45 лет
                return "35:47"


def get_mcv_norm(age, gender):
    """Возвращает норму среднего объема эритроцита (MCV) в зависимости от возраста и пола."""
    if age < 2 / 52:  # < 2 недели
        return "88:140"
    elif age < 1 / 12:  # 2 недели - 1 месяц
        return "91:112"
    elif age < 2 / 12:  # 1 - 2 месяца
        return "84:106"
    elif age < 4 / 12:  # 2 - 4 месяца
        return "76:97"
    elif age < 6 / 12:  # 4 - 6 месяцев
        return "68:85"
    elif age < 9 / 12:  # 6 - 9 месяцев
        return "70:85"
    elif age < 2:  # 9 месяцев - 2 года
        return "71:84"
    elif age < 5:  # 2 года - 5 лет
        return "73:85"
    elif age < 9:  # 5 - 9 лет
        return "75:87"
    elif age < 12:  # 9 - 12 лет
        return "76:90"
    elif age < 15:  # 12 - 15 лет
        if gender == 1:  # Мужчины
            return "77:94"
        else:  # Женщины
            return "73:95"
    elif age < 18:  # 15 - 18 лет
        if gender == 1:  # Мужчины
            return "79:95"
        else:  # Женщины
            return "78:98"
    else:
        # Норма для взрослых
        if gender == 1:  # Мужчины
            if 18 <= age <= 45:
                return "80:99"
            elif 45 <= age <= 65:
                return "81:101"
            else:  # > 65 лет
                return "81:103"
        else:  # Женщины
            if 18 <= age <= 45:
                return "81:100"
            elif 45 <= age <= 65:
                return "81:101"
            else:  # > 65 лет
                return "81:102"

def get_mch_norm(age, gender):
    """Возвращает норму среднего содержания гемоглобина в эритроците (MCH) в зависимости от возраста и пола."""
    if age < 2 / 52:  # < 2 недели
        return "30:37"
    elif age < 1 / 12:  # 2 недели - 1 месяц
        return "29:36"
    elif age < 2 / 12:  # 1 - 2 месяца
        return "27:34"
    elif age < 4 / 12:  # 2 - 4 месяца
        return "25:32"
    elif age < 6 / 12:  # 4 - 6 месяцев
        return "24:30"
    elif age < 9 / 12:  # 6 - 9 месяцев
        return "25:30"
    elif age < 1:  # 9 месяцев - 1 год
        return "24:30"
    elif age < 3:  # 1 - 3 года
        return "22:30"
    elif age < 9:  # 3 - 9 лет
        return "25:31"
    elif age < 15:  # 9 - 15 лет
        return "26:32"
    elif age < 18:  # 15 - 18 лет
        if gender == 1:  # Мужчины
            return "27:32"
        else:  # Женщины
            return "26:34"
    else:
        # Норма для взрослых
        if gender == 1:  # Мужчины
            if 18 <= age <= 45:
                return "27:34"
            elif 45 <= age <= 65:
                return "27:35"
            else:  # > 65 лет
                return "27:34"
        else:  # Женщины
            if 18 <= age <= 45:
                return "27:34"
            elif 45 <= age <= 65:
                return "27:34"
            else:  # > 65 лет
                return "27:35"

def get_mchc_norm(age, gender):
    """Возвращает норму средней концентрации гемоглобина в эритроците (MCHC) в зависимости от возраста и пола."""
    if age < 1 / 12:  # 1 день - 1 месяц
        return "316:375"
    elif age < 5 / 12:  # 2 - 5 месяцев
        return "306:324"
    elif age < 7 / 12:  # 6 - 7 месяцев
        return "307:324"
    elif age < 1:  # 8 месяцев - 1 год
        return "297:324"
    elif age < 3:  # 2 года
        return "307:344"
    elif age < 10:  # 3 - 9 лет
        return "336:344"
    elif age < 15:  # 10 - 14 лет
        return "336:354"
    elif age < 18:  # 15 - 18 лет
        return "300:380"
    else:
        # Норма для взрослых, независимо от пола
        return "300:380"

def get_rbc_norm(age, gender):
    """Возвращает норму эритроцитов (RBC) в зависимости от возраста и пола."""
    if age < 1 / 12:  # 1–13 дней
        return "3.9:5.9"
    elif age < 1:  # 14–30 дней, до 1 года
        if age < 2 / 12:
            return "3.3:5.3"
        elif age < 3 / 12:
            return "3.5:5.1"
        elif age < 4 / 12:
            return "3.6:4.8"
        elif age < 5 / 12:
            return "3.8:4.6"
        elif age < 6 / 12:
            return "4.0:4.8"
        elif age < 10 / 12:
            return "3.8:4.6"
        else:
            return "3.9:4.7"
    elif age < 5:  # 1 - 5 лет
        return "4.0:4.4"
    elif age == 6:
        return "4.1:4.5"
    elif age == 7:
        return "4.0:4.4"
    elif age == 8:
        return "4.2:4.6"
    elif age == 9:
        return "4.1:4.5"
    elif age < 12:  # 10 - 11 лет
        return "4.2:4.6"
    elif age < 15:  # 12–14 лет
        if gender == 1:  # Мальчики
            return "4.1:5.2"
        else:  # Девочки
            return "3.8:5.0"
    elif age < 18:  # 15–18 лет
        if gender == 1:  # Юноши
            return "4.2:5.6"
        else:  # Девушки
            return "3.9:5.1"
    else:
        # Норма для взрослых
        if gender == 1:  # Мужчины
            if 18 <= age <= 44:
                return "4.3:5.7"
            elif 45 <= age <= 64:
                return "4.2:5.6"
            else:  # > 65 лет
                return "3.8:5.8"
        else:  # Женщины
            if 18 <= age <= 44:
                return "3.8:5.1"
            elif 45 <= age <= 64:
                return "3.8:5.3"
            else:  # > 65 лет
                return "3.8:5.2"

def get_plt_norm(age):
    """Возвращает норму тромбоцитов (PLT) в зависимости от возраста."""
    # Нормы для детей до 1 года
    if age < 1 / 12:
        return "208:410"
    elif age < 2 / 12:
        return "208:352"
    elif age < 3 / 12:
        return "207:373"
    elif age < 4 / 12:
        return "205:395"
    elif age < 5 / 12:
        return "205:375"
    elif age < 6 / 12:
        return "203:377"
    elif age < 7 / 12:
        return "206:374"
    elif age < 8 / 12:
        return "215:365"
    elif age < 9 / 12:
        return "199:361"
    elif age < 10 / 12:
        return "205:355"
    elif age < 11 / 12:
        return "203:357"
    elif age < 1:
        return "207:353"
    
    # Нормы для детей старше 1 года
    elif age < 2:
        return "218:362"
    elif age < 3:
        return "214:366"
    elif age < 4:
        return "209:351"
    elif age < 5:
        return "196:344"
    elif age < 6:
        return "208:332"
    elif age < 7:
        return "220:360"
    elif age < 8:
        return "205:355"
    elif age < 9:
        return "205:375"
    elif age < 10:
        return "217:343"
    elif age < 11:
        return "211:349"
    elif age < 12:
        return "198:342"
    elif age < 13:
        return "202:338"
    elif age < 14:
        return "192:328"
    elif age < 15:
        return "198:342"
    elif age < 16:
        return "200:360"
    elif age < 17:
        return "180:320"
    
    # Норма для взрослых (с 18 лет и старше)
    return "180:320"

def get_wbc_norm(age, gender):
    """Возвращает норму лейкоцитов (WBC) в зависимости от возраста и пола."""
    # Нормы для детей
    if age < 10 / 12:
        return "6.0:17.5"
    elif age < 8:
        return "5.5:15.5"
    elif age < 12:
        return "4.5:13.5"
    elif age < 15:
        return "4.5:13.0"
    elif age < 18:
        return "4.5:11.3"
    
    # Нормы для мужчин
    if gender == 1:  # Мужчины
        if 12 <= age <= 16:
            return "4.5:13.0"
        else:
            return "4.5:11.3"
    
    # Нормы для женщин
    else:  # Женщины
        if 12 <= age <= 16:
            return "4.5:13.0"
        else:
            return "4.5:11.3"

def get_pct_norm(age):
    """Возвращает норму тромбокрита (PCT) в зависимости от возраста."""
    # Нормы для детей до 18 лет
    if age < 18:
        return "0.15:0.35"
    # Норма для взрослых
    else:
        return "0.15:0.4"

def get_ly_rel_norm(age, gender):
    if age <= 1 / 12:  # до 1 месяца
        return '25:60'
    elif 1 / 12 < age <= 1:  # 2–12 месяцев
        return '40:70'
    elif 1 < age <= 5:  # 1–5 лет
        return '35:60'
    elif 5 < age <= 10:  # 5–10 лет
        return '30:50'
    elif 10 < age <= 14:  # 10–14 лет
        return '30:48'
    elif age > 14:  # > 14 лет
        return '22:45'
    else:
        return None  # В случае, если возраст не попадает ни в одну категорию

def get_ly_abs_norm(age, gender):
    if age <= 1 / 12:  # до 1 месяца
        return '1.25:12.6'
    elif 1 / 12 < age <= 1:  # 2–12 месяцев
        return '2.2:12.3'
    elif 1 < age <= 5:  # 1–5 лет
        return '1.9:9.3'
    elif 5 < age <= 10:  # 5–10 лет
        return '1.3:7.3'
    elif 10 < age <= 14:  # 10–14 лет
        return '1.3:6.2'
    elif age > 14:  # > 14 лет (взрослые)
        return '1.0:4.0'
    else:
        return None  # В случае, если возраст не попадает ни в одну категорию

def get_ne_rel_norm(age, gender):
    if age <= 1 / 12:  # до 1 месяца
        return '31:55'
    elif 1 / 12 < age <= 1:  # 2–12 месяцев
        return '17:50'
    elif 1 < age <= 5:  # 1–5 лет
        return '30:60'
    elif 5 < age <= 10:  # 5–10 лет
        return '40:62'
    elif 10 < age <= 14:  # 10–14 лет
        return '44:65'
    elif age > 14:  # > 14 лет (взрослые)
        return '47:77'
    else:
        return None  # В случае, если возраст не попадает ни в одну категорию

def get_ne_abs_norm(age, gender):
    if age <= 1 / 12:  # до 1 месяца
        return '1.5:11.5'
    elif 1 / 12 < age <= 1:  # 2–12 месяцев
        return '0.9:8.8'
    elif 1 < age <= 5:  # 1–5 лет
        return '1.5:9.3'
    elif 5 < age <= 10:  # 5–10 лет
        return '1.8:8.1'
    elif 10 < age <= 14:  # 10–14 лет
        return '1.9:7.5'
    elif age > 14:  # > 14 лет (взрослые)
        return '1.8:7.2'
    else:
        return None  # В случае, если возраст не попадает ни в одну категорию

# Функция для определения нормы относительного количества моноцитов на основе возраста
def get_mo_rel_norm(age):
    if age <= 1 / 12:  # до 1 месяца
        return '5:15'
    elif 1 / 12 < age <= 1:  # 2–12 месяцев
        return '4:10'
    elif 1 < age <= 14:  # 1–14 лет
        return '3:11'
    elif age > 14:  # > 14 лет (взрослые)
        return '2:12'
    else:
        return None  # В случае, если возраст не попадает ни в одну категорию

def get_esr_norm(age, gender):
    if age < 10:  # Дети до 10 лет
        return '2:10'
    elif gender == 1:  # Мужчины
        if age < 50:
            return '1:15'
        else:
            return '2:20'
    elif gender == 0:  # Женщины
        if age < 50:
            return '2:20'
        else:
            return '2:30'
    else:
        return None  # В случае, если возраст или пол не указаны

def get_segm_neut_norm(age):
    """Возвращает норму сегментоядерных нейтрофилов в зависимости от возраста и пола."""
    if age < 16:
        # Норма для детей до 16 лет
        if 0 <= age <= 13 / 365:  # до 13 дней
            return "17:39"
        elif age < 1:  # дети до 1 года
            return "30:50"
        elif age < 2:  # дети 1 год 
            return "23:43"
        elif age < 3:  # дети 2 лет
            return "28:48"
        elif 2 < age < 5:  # дети 3-4 лет
            return "32:54"
        elif 4 < age < 8:  # дети 5-7 лет
            return "35:58"
        elif 7 < age < 12:  # дети 8-11 лет 
            return "41:59"
        else:  # все дети до 16 лет
            return "44:61"
    else: # норма для всех взрослых и детей старше 16
        return "47:72"

def get_mpv_norm():
    """Возвращает норму среднего объема тромбоцитов (MPV)."""
    return "7.8:11.0"

def get_rdw_norm():
    """Возвращает норму распределения эритроцитов (RDW)."""
    return "10:18"

def get_rdw_sd_norm():
    """Возвращает норму стандартного отклонения RDW (RDW_SD)."""
    return "35:60"

def get_rdw_cv_norm():
    """Возвращает норму коэффициента вариации RDW (RDW_CV)."""
    return "10:18"

def get_pdw_norm():
    """Возвращает норму распределения тромбоцитов по объему (PDW)."""
    return "9.0:17.0"

def get_eo_rel_norm():
    """Возвращает норму относительного содержания эозинофилов (EO_REL)."""
    return "0.0:5.0"

def get_eo_abs_norm():
    """Возвращает норму абсолютного содержания эозинофилов (EO_ABS)."""
    return "0.00:0.40"

def get_ba_rel_norm():
    """Возвращает норму относительного содержания базофилов (BA_REL)."""
    return "0.0:2.0"

def get_ba_abs_norm():
    """Возвращает норму абсолютного содержания базофилов (BA_ABS)."""
    return "0.00:0.10"

def get_mo_abs_norm():
    """Возвращает норму абсолютного содержания моноцитов (MO_ABS)."""
    return "0.10:0.70"

def get_band_neut_norm():
    """Возвращает норму содержания палочкоядерных нейтрофилов (BAND_NEUT)."""
    return "1:6"

def get_ly_leico_norm():
    """Возвращает норму содержания лимфоцитов в лейкоцитарной формуле (LY_LEICO)."""
    return "18:44"

def get_mo_leico_norm():
    """Возвращает норму содержания моноцитов в лейкоцитарной формуле (MO_LEICO)."""
    return "2:12"

def get_eo_leico_norm():
    """Возвращает норму содержания эозинофилов в лейкоцитарной формуле (EO_LEICO)."""
    return "0:5"

def get_ba_leico_norm():
    """Возвращает норму содержания базофилов в лейкоцитарной формуле (BA_LEICO)."""
    return "0:2"
