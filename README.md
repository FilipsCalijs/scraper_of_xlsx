
# Bulk Domain Status Checker from Excel
проще говоря: скрипт проверяет - работает ли сайт, все ли с ним хорошо и какой статус у страницы

## Purpose

This script automatically checks the HTTP/HTTPS status of domains listed in an Excel file (.xlsx).
It scans all worksheets until it reaches a sheet named "uprankd", collects unique domains from the second column (column B),
and then checks each domain's availability using several URL variations.

## Required Files

- One Excel file (.xlsx) located in the same folder where the script is run
- Domains must be listed in the second column (B) of each worksheet
- A worksheet named "uprankd" is used as a stop signal

## Dependencies

You will need the following Python libraries:

- pandas
- requests
- openpyxl

Install them using:

```
pip install pandas requests openpyxl
```

## Output Files

- `all_domains.txt` – list of all unique domains collected from Excel
- `domains_working.txt` – domains that returned status 403 (restricted but reachable)
- `domains_problem.txt` – domains that returned errors (404, 500, or failed to connect)
- Excel `.xlsx` file – input file used to extract domains

## Example Console Output

```
Found Excel file: Minisites Management.xlsx
Reading sheet: LV
Added 211 domains from sheet: LV
Reading sheet: LT
Added 33 domains from sheet: LT
Sheet 'uprankd' found. Stopping processing.
Unique domains to check: 1190
All domains saved to: all_domains.txt

Done — domains with status 200: 842
403 statuses saved to: domains_working.txt — 211
Errors/problems saved to: domains_problem.txt — 137
```






# Скрипт массовой проверки статусов доменов из Excel

## Назначение

Скрипт предназначен для автоматической проверки статусов доменов, указанных в Excel-файле (.xlsx).
Он проходит по листам до первого названия "uprankd", собирает уникальные домены из второго столбца (колонка B),
а затем проверяет их доступность по HTTP/HTTPS.

## Какие файлы необходимы

- Один Excel-файл в формате .xlsx, расположенный в той же папке, где запускается скрипт
- Во втором столбце (B) должны находиться домены
- Лист с названием "uprankd" используется как точка остановки

## Что может потребоваться установить (зависимости)

Для работы скрипта нужны библиотеки:

- pandas
- requests
- openpyxl

Установка (если нужно):

```
pip install pandas requests openpyxl
```

## Используемые файлы

- `all_domains.txt` – список всех уникальных доменов, собранных из Excel
- `domains_working.txt` – домены, ответившие со статусом 403
- `domains_problem.txt` – домены с ошибками (404, 500 и др.), а также те, что не ответили
- Excel-файл `.xlsx` – исходный файл с вкладками, откуда берутся домены

## Финальный пример вывода в консоли

```
Найден Excel-файл: Minisites Management.xlsx
Чтение листа: LV
Добавлено 211 доменов из листа: LV
Чтение листа: LT
Добавлено 33 доменов из листа: LT
Обнаружен лист 'uprankd'. Прекращаю обработку.
Уникальных доменов для проверки: 1190
Все домены сохранены в: all_domains.txt

Готово — доменов с 200 статусом: 842
Статусы 403 сохранены в: domains_working.txt — 211
Ошибки/проблемы — в: domains_problem.txt — 137
```
