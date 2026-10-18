# Структура репозитория для лабораторных работ семестра

**Студент:** Геграев Ислам Русланович
**Группа:** ПИЖ-б-о-25-2

### Команды создания и настройки проекта

```bash
python -m venv venv
venv\Scripts\activate
pip install Django
django-admin startproject MySite
cd MySite
python manage.py runserver
python manage.py startapp news
```

### Описание ключевых файлов и папок

```
labs/
├── .venv/                     # Виртуальное окружение Python
├── MySite/
│   ├── MySite/                # Главный конфигурационный пакет проекта
│   │   ├── __init__.py
│   │   ├── settings.py        # Настройки проекта (подключение БД, константы MEDIA)
│   │   ├── urls.py            # Корневые маршруты (добавлено обслуживание медиафайлов)
│   │   ├── wsgi.py
│   │   └── asgi.py
│   ├── news/                  # Приложение "Новости"
│   │   ├── __init__.py
│   │   ├── admin.py           # Настройки административной панели
│   │   ├── apps.py
│   │   ├── models.py          # Описание моделей данных (классы News и Order)
│   │   ├── views.py           
│   │   ├── urls.py            
│   │   └── migrations/        # Папка с файлами миграций структуры БД
│   │       ├── 0001_initial.py # Автоматическая миграция для создания модели News
│   │       └── 0002_order.py  # Последующие миграции для модели Order
│   ├── db.sqlite3             # Файл базы данных SQLite3 с созданными таблицами
│   └── manage.py              # Скрипт управления проектом Django
└── Readme.md                  
```
