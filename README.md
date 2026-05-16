# TGBudgetBot

Телеграм-бот для ведения личного и общего бюджета с синхронизацией в Google Sheets.

---

# Возможности

* Быстрое внесение расходов
* Режимы:

  * Личное
  * Общее
* Категории через кнопки
* Быстрый ручной ввод
* Комментарии к операциям
* Локальная SQLite база
* Синхронизация с Google Sheets
* FSM flow для удобного ввода
* Ограничение доступа по Telegram ID

---

# Примеры использования

## Быстрый ввод

```text
мак 12 бигмак
```

## Guided flow

```text
/start
↓
Личное
↓
🍔 Еда
↓
12
↓
бургер
```

---

# Структура проекта

```text
bot/
│
├── handlers/
│   ├── start.py
│   ├── reset.py
│   ├── mode.py
│   ├── category.py
│   └── text.py
│
├── services/
│   ├── google_sheets.py
│   └── sync_service.py
│
├── database/
│   ├── database.py
│   └── init_db.py
│
├── models/
│   └── expense.py
│
├── utils/
│   ├── access.py
│   ├── categories.py
│   ├── keyboards.py
│   └── parser.py
│
├── config.py
│
main.py
```

---

# Стек

* Python
* python-telegram-bot
* SQLAlchemy
* SQLite
* gspread
* Google Sheets API

---

# Установка

## 1. Клонировать проект

```bash
git clone <repo>
```

---

## 2. Создать venv

```bash
python -m venv .venv
```

---

## 3. Активировать venv

### Windows

```bash
.venv\Scripts\activate
```

### Linux/macOS

```bash
source .venv/bin/activate
```

---

## 4. Установить зависимости

```bash
pip install -r requirements.txt
```

---

# ENV

Создать `.env`

```env
BOT_TOKEN=your_token

FIRST_ID=123456
SECOND_ID=654321
```

---

# Google Sheets

## Нужно:

* Google Cloud Project
* Service Account
* Google Sheets API
* Google Drive API

---

## credentials

Файл:

```text
credentials/google.json
```

---

## Не забыть:

Поделиться таблицей с:

```text
client_email
```

из service account json.

---

# Запуск

```bash
python main.py
```

---

# Команды

| Команда  | Описание        |
| -------- | --------------- |
| `/start` | старт           |
| `/reset` | сброс состояния |

---

# Планируемые функции

* История операций
* Undo/delete
* Inline buttons
* OCR чеков
* AI parser
* Аналитика
* Автокатегоризация
* Dashboard
* Monthly reports
* Export/import
* Multi-user support

---

# Архитектура

Бот использует FSM-подход:

```text
mode
↓
category
↓
amount
↓
comment
↓
save
```

Также поддерживается quick input mode без FSM.

---

# Автор

роня + suffering 😭
