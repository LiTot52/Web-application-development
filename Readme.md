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
├── venv/                     
├── MySite/
│   ├── MySite/                
│   │   ├── __init__.py
│   │   ├── settings.py       
│   │   ├── urls.py           
│   │   ├── wsgi.py
│   │   └── asgi.py
│   ├── news/                  
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── views.py           
│   │   ├── urls.py            
│   │   └── migrations/
│   ├── db.sqlite3            
│   └── manage.py              
└── Readme.md                  

```

| Файл/папка     | Назначение                                                |
| -------------- | --------------------------------------------------------- |
| README.md      | Главный файл курса с описанием, списком работ, навигацией |
| news/views.py  | Контроллеры приложения                                    |
| news/urls.py   | Маршруты приложения                                       |
| MySite/urls.py | Корневые маршруты проекта                                 |
| settings.py    | Настройки проекта, регистрация приложений                 |
