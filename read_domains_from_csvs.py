import os
import pandas as pd
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

# === Поиск первого .xlsx-файла ===
xlsx_files = [f for f in os.listdir('.') if f.lower().endswith('.xlsx')]
if not xlsx_files:
    print("❌ Нет .xlsx файла в папке.")
    exit()

excel_file = xlsx_files[0]
print(f"📁 Найден Excel-файл: {excel_file}")

# === Файлы вывода ===
all_domains_file = 'all_domains.txt'
working_file = 'domains_sus(403).txt'
problem_file = 'domains_problem.txt'
MAX_THREADS = 20
TIMEOUT = 3

print("⚙️ Начинаю работу. Пожалуйста, не выключайте компьютер...")

# === Открытие Excel ===
xls = pd.ExcelFile(excel_file)
sheet_names = xls.sheet_names

seen_domains = set()
new_domains = []

for sheet_name in sheet_names:
    if sheet_name.lower() == 'uprankd':
        print(f"🛑 Обнаружен лист 'uprankd'. Прекращаю обработку.")
        break

    print(f"📄 Чтение листа: {sheet_name}")
    df = pd.read_excel(xls, sheet_name=sheet_name)

    if df.shape[1] < 2:
        continue

    col_b = df.iloc[:, 1]

    added = 0
    for val in col_b:
        if pd.isna(val):
            continue
        domain = str(val).strip()
        if not domain or domain in seen_domains:
            continue
        seen_domains.add(domain)
        new_domains.append(domain)
        added += 1

    print(f"➕ Добавлено {added} доменов из листа: {sheet_name}")

print(f"🔢 Уникальных доменов для проверки: {len(new_domains)}")

# === Сохранение всех уникальных доменов ===
with open(all_domains_file, "w", encoding="utf-8") as f:
    for domain in new_domains:
        f.write(domain + "\n")

print(f"📄 Все домены сохранены в: {all_domains_file}")

# === Генерация URL-вариантов ===
def generate_urls(domain):
    return [
        f"http://{domain}",
        f"http://www.{domain}",
        f"https://{domain}",
        f"https://www.{domain}"
    ]

# === Проверка одного домена ===
def check_domain(domain):
    urls = generate_urls(domain)
    for url in urls:
        try:
            response = requests.head(url, timeout=TIMEOUT, allow_redirects=True)
            if response.status_code == 200:
                return ("ok200", f"{domain} - 200 ({url})")
            elif response.status_code == 403:
                return ("ok403", f"{domain}")
            else:
                return ("fail", f"{domain} - {response.status_code} ({url})")
        except Exception:
            continue
    return ("fail", f"{domain} - Error")

# === Загрузка из all_domains.txt ===
with open(all_domains_file, "r", encoding="utf-8") as f:
    domains = [line.strip() for line in f if line.strip()]

# === Проверка статусов параллельно ===
ok_200 = []
ok_403 = []
fail = []

with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
    future_map = {executor.submit(check_domain, domain): domain for domain in domains}

    for future in as_completed(future_map):
        status, result = future.result()
        if status == "ok200":
            ok_200.append(result)
        elif status == "ok403" and result:
            ok_403.append(result)
        elif status == "fail" and result:
            fail.append(result)

# === Сохранение результатов ===
with open(working_file, "w", encoding="utf-8") as f_ok:
    for line in ok_403:
        f_ok.write(line + "\n")

with open(problem_file, "w", encoding="utf-8") as f_fail:
    for line in fail:
        f_fail.write(line + "\n")

# === Вывод статистики ===
print(f"\n✅ Готово — доменов с 200 статусом: {len(ok_200)}")
print(f"🟡 Статусы 403 сохранены в: {working_file} — {len(ok_403)}")
print(f"🔴 Ошибки/проблемы — в: {problem_file} — {len(fail)}")
