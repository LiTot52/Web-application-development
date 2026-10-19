# Лабораторная работа №3: Шаблоны. Админка Django

**Студент:** Геграев Ислам Русланович  
**Группа:** ПИЖ-б-о-25-2  
**Технология:** Python + Django

## Содержание
- [Лабораторная работа №3: Шаблоны. Админка Django](#лабораторная-работа-3-шаблоны-админка-django)
	- [Содержание](#содержание)
	- [Цель работы](#цель-работы)
	- [Теоретическое обоснование](#теоретическое-обоснование)
	- [Выполнение практического примера](#выполнение-практического-примера)
		- [Описание ключевых файлов и папок](#описание-ключевых-файлов-и-папок)
		- [Скриншоты работы](#скриншоты-работы)
		- [Результаты проверки](#результаты-проверки)
	- [Ответы на контрольные вопросы](#ответы-на-контрольные-вопросы)
	- [Вывод](#вывод)
	- [Рекомендуемые источники](#рекомендуемые-источники)


## Цель работы

Научиться использовать шаблоны Django для отображения данных модели в браузере и настраивать административную панель для управления записями приложения.

## Теоретическое обоснование

**Шаблон (Template)** - HTML-файл, в котором с помощью шаблонизатора Django можно отображать данные, переданные из представления.

**Представление (View)** - функция или класс, обрабатывающие запрос пользователя, получающие необходимые данные и возвращающие ответ. Для формирования HTML-страницы удобно использовать функцию `render()`.

**Контекст** - словарь с данными, которые передаются из представления в шаблон.

**Шаблонизатор Django** использует следующие элементы:

| Элемент    | Назначение                         | Пример                                    |
| ---------- | ---------------------------------- | ----------------------------------------- |
| Переменные | Вывод значений из контекста        | `{{ title }}`                             |
| Теги       | Управление формированием страницы  | `{% for item in news %}`                  |
| Фильтры    | Преобразование значения при выводе | `{{ item.created_at\|date:"d.m.Y H:i" }}` |

**Административная панель Django** - встроенный интерфейс для просмотра, добавления, изменения и удаления записей моделей. Доступна по адресу `/admin/`. Чтобы управлять моделью через админку, её необходимо зарегистрировать в `admin.py`.

**Настройка модели в админке** выполняется с помощью класса, наследуемого от `admin.ModelAdmin`. Например, `list_display` определяет столбцы списка, `list_display_links` — поля-ссылки для открытия записи, `search_fields` - поля, по которым выполняется поиск.

**Класс `Meta` модели** позволяет задавать дополнительные параметры. `verbose_name` определяет название модели в единственном числе, `verbose_name_plural` - во множественном, `ordering` - порядок сортировки записей.

**Медиафайлы** - загружаемые изображения и другие файлы. Для изображений применяется поле `ImageField`. Параметр `blank=True` позволяет не заполнять поле в форме. После изменения модели необходимо создать и применить миграции.

---

## Выполнение практического примера

 
**1. Контроллер.** В `news/views.py` импортирована модель `News`, получены все записи и передан контекст в шаблон через `render()`.
 
**`news/views.py`**
```python
from django.shortcuts import render
from django.http import HttpResponse
from .models import News
 
 
def index(request):
    news = News.objects.all()
    context = {'news': news, 'title': 'Список новостей'}
    return render(request, template_name='news/index.html', context=context)
 
 
def test(request):
    return HttpResponse('<h1>Тестовая страница</h1>')
```
 
**2. Шаблон.** В приложении `news` создана папка `templates`, а в ней вложенная папка `news` (пространство имён, чтобы шаблоны разных приложений не конфликтовали). В неё добавлен файл `index.html`: переменные выводят заголовок и поля записи, тег `for` перебирает новости, фильтр `date` форматирует дату.
 
**`news/templates/news/index.html`**
```html
<!DOCTYPE html>
<html lang="en">
 
<head>
	<meta charset="UTF-8">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<title>{{ title }}</title>
</head>
 
<body>
	<h1>{{ title }}</h1>
 
	{% for item in news %}
	<div>
		<p>{{ item.title }}</p>
		<p>{{ item.content }}</p>
		<p>{{ item.created_at|date:"d.m.Y H:i" }}</p>
	</div>
	<hr>
	{% endfor %}
 
</body>
 
</html>
```
 
**3. Модель.** В `news/models.py` полям добавлены русские названия (`verbose_name`), поле `photo` сделано необязательным (`blank=True`), а в классе `Meta` заданы названия модели и сортировка от новых записей к старым. Сортировка в `Meta` действует и в админке, и на сайте, поэтому в контроллере достаточно `News.objects.all()`.
 
**`news/models.py`**
```python
from django.db import models
 
 
class News(models.Model):
    title = models.CharField(max_length=150, verbose_name='Наименование')
    content = models.TextField(blank=True, verbose_name='Контент')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d', verbose_name='Фото', blank=True)
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')

class Order(models.Model):
    customer_name = models.CharField(max_length=200)
    order_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False)
    delivery_address = models.TextField(blank=True)

    def __str__(self):
        return self.title
 
    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['-created_at']
```
 
**4. Админка.** Создан суперпользователь командой `python manage.py createsuperuser`. Модель зарегистрирована вместе с настраивающим классом `NewsAdmin`: заданы столбцы списка, поля-ссылки и поля поиска. Класс описывается до регистрации, а модель регистрируется только один раз.
 
**`news/admin.py`**
```python
from django.contrib import admin
from .models import News
 
 
class NewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_at', 'updated_at', 'is_published')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'content')
 
 
admin.site.register(News, NewsAdmin)
```
 
**5. Название раздела.** Чтобы вместо `NEWS` в админке отображалось русское название, в конфигурацию приложения добавлен `verbose_name`.
 
**`news/apps.py`**
```python
from django.apps import AppConfig
 
 
class NewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'news'
    verbose_name = 'Новости'
```
 
В `MySite/settings.py` приложение подключено как `'news.apps.NewsConfig'`, а язык интерфейса админки задан настройкой `LANGUAGE_CODE = 'ru'`.
 
**6. Миграции.** После изменения модели созданы и применены миграции:
 
```bash
python manage.py makemigrations
python manage.py migrate
```
 
При создании миграции Django запросил значение по умолчанию для нового поля `created_at` у уже существующих записей. Был выбран вариант `1` и введено `timezone.now`.
 



```
labs/
├── .venv/                     
├── MySite/
│   ├── media/                   
│   │   └── photos/
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
│   │   ├── templates/         
│   │   │   └── news/          
│   │   │       └── index.html 
│   │   └── migrations/        
│   │       ├── 0001_initial.py
│   │       ├── 0002_order.py
│   │       └── 0004_remove_news_created_ad_news_created_at_and_more     
│   ├── db.sqlite3             
│   └── manage.py             
└── Readme.md
 
```


---
### Описание ключевых файлов и папок
 
| Файл / Папка                         | Назначение и внесённые изменения                                                                                     |
| :----------------------------------- | :------------------------------------------------------------------------------------------------------------------- |
| **`news/views.py`**                  | Контроллер `index` получает записи модели и передаёт их в шаблон через `render()` вместе с контекстом.               |
| **`news/templates/news/`**           | Папка шаблонов приложения (вложенная папка `news` — пространство имён). Содержит `index.html`.                       |
| **`news/templates/news/index.html`** | Шаблон страницы: переменные `{{ }}`, тег `{% for %}`, фильтр `date`.                                                 |
| **`news/models.py`**                 | Добавлены `verbose_name` полям, `blank=True` для `photo`, класс `Meta` (названия модели и сортировка `-created_at`). |
| **`news/admin.py`**                  | Модель зарегистрирована с классом `NewsAdmin` (`list_display`, `list_display_links`, `search_fields`).               |
| **`news/apps.py`**                   | В `NewsConfig` добавлен `verbose_name = 'Новости'` для русского названия раздела в админке.                          |
| **`news/migrations/`**               | Добавлена миграция с изменениями модели `News`.                                                                      |
| **`MySite/settings.py`**             | Язык интерфейса изменён на русский (`LANGUAGE_CODE = 'ru'`).                                                         |

---

### Скриншоты работы
 
**1. `http://127.0.0.1:8000/news/` — страница со списком новостей.**
 
![Список новостей](/Лабы/Второй%20год/Web-разработка/Web-application-development/labs/screenshots/labs-3/01-news-list.png)
 
**2. `http://127.0.0.1:8000/admin/` — вход в админку.**
 
![Вход в админку](/Лабы/Второй%20год/Web-разработка/Web-application-development/labs/screenshots/labs-3/02-admin-login.png)
 
**3. Список новостей в админке (столбцы, поиск, русские названия).**
 
![Список в админке](/Лабы/Второй%20год/Web-разработка/Web-application-development/labs/screenshots/labs-3/03-admin-list.png)
 
**4. Добавление новости без фото.**
 
![Добавление новости](/Лабы/Второй%20год/Web-разработка/Web-application-development/labs/screenshots/labs-3/04-admin-add.png)
 
### Результаты проверки
 
| Адрес                              | Результат                                                     |
| ---------------------------------- | ------------------------------------------------------------- |
| `http://127.0.0.1:8000/news/`      | Список новостей от новых к старым, дата в формате `д.м.Г Ч:М` |
| `http://127.0.0.1:8000/news/test/` | «Тестовая страница»                                           |
| `http://127.0.0.1:8000/admin/`     | Вход в админку, раздел «Новости» с настроенным списком        |

## Ответы на контрольные вопросы

1. **Что такое шаблон в Django?** - Это HTML-файл, в который Django подставляет данные и в котором можно использовать переменные, теги и фильтры шаблонизатора.

2. **Для чего используется функция `render()`?** - Она принимает объект запроса, имя шаблона и необязательный контекст, после чего возвращает HTTP-ответ с отрендеренной HTML-страницей.

3. **Что такое контекст шаблона?** - Словарь, содержащий данные, которые представление передаёт шаблону для отображения.

4. **Чем отличаются переменные, теги и фильтры шаблонизатора?** - Переменные выводят значения (`{{ title }}`), теги управляют логикой вывода (`{% for %}`, `{% if %}`), а фильтры преобразуют значения (`{{ date|date:"d.m.Y" }}`).

5. **Где Django ищет шаблоны приложения по умолчанию?** - В каталоге `templates` приложения. Для изоляции шаблонов рекомендуется создавать внутри него папку с именем приложения, например `templates/news/`.

6. **Как получить все записи модели и отсортировать их по дате?** - Получить записи можно через `News.objects.all()`, а отсортировать - например, через `News.objects.order_by('-created_at')`. Имя поля должно соответствовать модели.

7. **Как открыть административную панель Django?** - Запустить сервер, открыть `/admin/` и войти под суперпользователем, созданным командой `python manage.py createsuperuser`.

8. **Как добавить модель в административную панель?** - Импортировать её в `admin.py` и зарегистрировать через `admin.site.register(News)` или декоратор `@admin.register(News)`.

9. **Для чего нужен класс `admin.ModelAdmin`?** - Он позволяет настраивать отображение модели в админке, в том числе столбцы списка (`list_display`), ссылки (`list_display_links`) и поля поиска (`search_fields`).

10. **Для чего используется класс `Meta` в модели?** - Для задания дополнительных параметров, например отображаемых названий модели (`verbose_name`, `verbose_name_plural`) и сортировки по умолчанию (`ordering`).

11. **Чем отличаются `blank=True` и `null=True`?** - `blank=True` разрешает не заполнять поле при валидации формы, а `null=True` разрешает хранить в соответствующем столбце базы данных значение `NULL`.

12. **Как настроить загрузку изображений?** - Использовать `ImageField`, установить Pillow, задать `MEDIA_ROOT` и `MEDIA_URL`, а в корневом `urls.py` подключить раздачу медиафайлов для режима разработки. После изменения модели нужно выполнить миграции.

## Вывод

В ходе лабораторной работы рассмотрены шаблоны Django и способы передачи данных из представления в HTML-страницу. Освоены переменные, теги и фильтры шаблонизатора, вывод и сортировка записей модели. Также выполнена регистрация модели в административной панели, изучены настройки отображения, поиска, названий и сортировки. Рассмотрена настройка загрузки изображений и применение миграций после изменения модели.

## Рекомендуемые источники

1. **Официальная документация Django** - https://docs.djangoproject.com/
2. **Django: шаблоны** - https://docs.djangoproject.com/en/stable/topics/templates/
3. **Django: административная панель** - https://docs.djangoproject.com/en/stable/ref/contrib/admin/
4. **Django: модели** - https://docs.djangoproject.com/en/stable/topics/db/models/
5. **Django: управление статическими и медиафайлами** - https://docs.djangoproject.com/en/stable/howto/static-files/