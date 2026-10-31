# Лабораторная работа №4: Связи моделей. Внешний вид шаблона

**Студент:** Геграев Ислам Русланович  
**Группа:** ПИЖ-б-о-25-2  
**Вариант:** 10
**Технология:** Python + Django

## Содержание
- [Лабораторная работа №4: Связи моделей. Внешний вид шаблона](#лабораторная-работа-4-связи-моделей-внешний-вид-шаблона)
  - [Содержание](#содержание)
  - [Цель работы](#цель-работы)
  - [Теоретическое обоснование](#теоретическое-обоснование)
    - [Файлы папки](#файлы-папки)
    - [Команды для запуска](#команды-для-запуска)
  - [Выполнение практического примера](#выполнение-практического-примера)
    - [Скриншоты](#скриншоты)
  - [Вывод](#вывод)
  - [Ответы на контрольные вопросы](#ответы-на-контрольные-вопросы)
  - [Рекомендуемые источники](#рекомендуемые-источники)


## Цель работы

Освоить создание и настройку связей между моделями Django (`ForeignKey`, `ManyToManyField`, `OneToOneField`), изучить параметры связей (`on_delete`, `related_name`, `null`, `blank`, `default`), научиться применять миграции при добавлении связей к существующим моделям, а также настраивать отображение связанных данных в административной панели Django.

## Теоретическое обоснование

**Нормализация данных.** Хранить всё в одной таблице неудобно: название категории пришлось бы дублировать в каждой новости, а при переименовании - менять во всех строках. Поэтому категории выносят в отдельную таблицу, а в таблице новостей хранят только номер категории - **внешний ключ**. Переименовать категорию тогда можно один раз.

**Первичная и вторичная модель.** Первичная (главная) модель - та, на которую ссылаются (`Category`). Вторичная (зависимая) - та, где объявлено поле связи (`News`). Первичную модель нужно объявлять **раньше** вторичной либо ссылаться на неё строкой: `ForeignKey('Category', ...)`.

**Типы связей в Django:**

| Поле              | Тип связи        | Пример                                 |
| ----------------- | ---------------- | -------------------------------------- |
| `ForeignKey`      | многие-к-одному  | много новостей - одна категория        |
| `ManyToManyField` | многие-ко-многим | пост - много тегов, тег - много постов |
| `OneToOneField`   | один-к-одному    | пользователь - один профиль            |

Поле связи записывается во **вторичной** модели.

**Параметры связи:**

| Параметр       | Назначение                                                                                  |
| -------------- | ------------------------------------------------------------------------------------------- |
| `on_delete`    | Что делать с зависимыми объектами при удалении объекта, на который они ссылаются            |
| `related_name` | Имя обратной связи: `category.news.all()` вместо `category.news_set.all()`                  |
| `null=True`    | В столбце БД допускается `NULL`                                                             |
| `blank=True`   | Поле можно не заполнять в формах и админке (валидация)                                      |
| `default`      | Значение по умолчанию (для `ForeignKey` - id существующей записи, иначе ошибка целостности) |
| `db_index`     | Создаёт индекс для ускорения поиска (первичный ключ индексируется по умолчанию)             |

**Значения `on_delete`** (из `django.db.models`, указываются без скобок - Django вызывает их сам):

| Значение   | Поведение                                                                                    |
| ---------- | -------------------------------------------------------------------------------------------- |
| `CASCADE`  | Каскадное удаление: вместе с объектом удаляются все зависимые                                |
| `PROTECT`  | Запрещает удаление, вызывая `ProtectedError` (подкласс `IntegrityError`)                     |
| `RESTRICT` | Запрещает удаление через `RestrictedError`, но допускает его, если объект удаляется каскадно |
| `SET_NULL` | Записывает в поле `NULL` (требует `null=True`)                                               |

**Строковое представление `__str__`** возвращает осмысленное имя объекта. Без него в выпадающем списке админки отображается `Category object (1)`.

**Настройка админки для связанных данных:** `list_display` (в том числе поле-связь), `list_filter` (фильтр по категории), `list_editable` (редактирование прямо в списке), `search_fields`, `prepopulated_fields` (автозаполнение `slug`).

---


### Файлы папки
```
labs/
├── .venv/
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
│   │   ├── templates/
│   │   │   └── news/
│   │   │       └── index.html
│   │   └── migrations/
│   │       ├── 0001_initial.py
│   │       ├── 0002_order.py
│   │       ├── 0003_alter_order_customer_name.py
│   │       ├── 0004_remove_news_created_ad_news_created_at_and_more.py
│   │       └── 0005_category_alter_news_options_news_category.py
│   ├── db.sqlite3
│   └── manage.py
└── Readme.md
```

### Команды для запуска

```bash
python manage.py makemigrations
python manage.py sqlmigrate news 0005
python manage.py migrate
python manage.py check
python manage.py runserver
```

---



## Выполнение практического примера


В файле `models.py` была спроектирована и реализована архитектура взаимосвязанных таблиц. Для сообщений добавлена каскадная связь `ForeignKey` с моделью тем форума. Также успешно решена задача интеграции поля для загрузки пользовательских медиафайлов `FileField` с поддержкой опционального заполнения (`blank=True, null=True`).

**`news/models.py`**

```python 

from django.db import models

# Create your models here.
# pip install
# Pillow


class Category(models.Model):
    title = models.CharField(
        max_length=150, db_index=True, verbose_name='Наименование товара')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['title']

    def __str__(self):
        return self.title


class News(models.Model):
    title = models.CharField(max_length=150, verbose_name='Наименование')
    content = models.TextField(blank=True, verbose_name='Контент')
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата публикации')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')
    photo = models.ImageField(
        upload_to='photos/%Y/%m/%d', verbose_name='Фото', blank=True)
    is_published = models.BooleanField(
        default=True, verbose_name='Опубликовано')
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, null=True, verbose_name='Категория')

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Order(models.Model):
    customer_name = models.CharField(max_length=200)
    order_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False)
    delivery_address = models.TextField(blank=True)

    def __str__(self):
        return f"Заказ №{self.id} - {self.customer_name}"


class Topic(models.Model):
    name = models.CharField(max_length=180, verbose_name='Название темы')
    author_name = models.CharField(max_length=100, verbose_name='Автор темы')
    create_date = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата создания')
    is_it_closed = models.BooleanField(
        default=False, verbose_name='Закрыта ли тема')

    class Meta:
        verbose_name = "Тема форума"
        verbose_name_plural = 'Темы форума'
        ordering = ['-create_date']

    def __str__(self):
        return self.name


class Message(models.Model):
    # ? связь с темой
    topic = models.ForeignKey(
        Topic, on_delete=models.CASCADE, verbose_name='Тема')
    text = models.CharField(max_length=200, verbose_name='Текст сообщения')
    author_name = models.CharField(
        max_length=180, verbose_name='Автор сообщения')
    date = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата отправки')
    file = models.FileField(upload_to='forum_files/',
                            blank=True, null=True, verbose_name='Файл')

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        ordering = ['date']

    def __str__(self):
        return f"Сообщение от {self.author_name} в теме '{self.topic.name}'"

```

В конфигурационном файле панели администратора `admin.py` разработан кастомный интерфейс для комфортного администрирования сущностей форума. Реализованы функции текстового поиска по содержимому и гибкие фильтры по временным меткам.

**`news/admin.py`**

```python


```


### Скриншоты

<details>
<summary><b>1. Главная страница админ-панели с разделами форума</b></summary>

![Разделы Темы и Сообщения в админке](/Лабы/Второй%20год/Web-разработка/Web-application-development/labs/screenshots/labs-4/01-admin-main.png)

</details>

<details>
<summary><b>2. Форма создания новой Темы форума</b></summary>

![Создание темы форума](/Лабы/Второй%20год/Web-разработка/Web-application-development/labs/screenshots/labs-4/02-topic-add.png)

</details>

<details>
<summary><b>3. Форма добавления нового Сообщения с прикреплением файла</b></summary>

![Добавление сообщения в тему](/Лабы/Второй%20год/Web-разработка/Web-application-development/labs/screenshots/labs-4/03-message-add.png)

</details>

<details>
<summary><b>4. Список сообщений в админке </b></summary>

![Поиск по тексту и фильтр по дате](/Лабы/Второй%20год/Web-разработка/Web-application-development/labs/screenshots/labs-4/04-message-list-filters.png)

</details>


## Вывод

В ходе лабораторной работы рассмотрены связи между моделями Django и параметры `ForeignKey`. Создана первичная модель `Category` и добавлена связь «одна категория - много новостей» с `on_delete=PROTECT`, `related_name`, `null=True` и `blank=True`. Создана и применена миграция, проверена структура БД: появились таблица `news_category` и внешний ключ `category_id`. Модели зарегистрированы в админке, настроены `list_display`, `list_filter`, `list_editable` и `search_fields`. Проверена защита от удаления категории с новостями. Трудности возникли из-за `__str__` и `Meta`, записанных вне класса, и из-за добавления обязательного поля в таблицу с данными; они устранены переносом кода в классы и применением `null=True`.

## Ответы на контрольные вопросы

1. **Зачем разделять данные по нескольким таблицам?** - Чтобы не нарушать нормализацию: данные не дублируются, а изменение (например, переименование категории) делается в одном месте.

2. **Какие типы связей есть в Django?** - `ForeignKey` (многие-к-одному), `ManyToManyField` (многие-ко-многим) и `OneToOneField` (один-к-одному).

3. **В какой модели записывается `ForeignKey`?** - Во вторичной (зависимой), то есть в той, где на одну запись главной модели приходится много записей (в `News`).

4. **Что делает параметр `on_delete`?** - Определяет поведение при удалении связанного объекта: `CASCADE` удаляет зависимые записи, `PROTECT` запрещает удаление, `RESTRICT` запрещает его с оговоркой для каскадных удалений, `SET_NULL` записывает `NULL`.

5. **Чем `PROTECT` отличается от `CASCADE`?** - `CASCADE` вместе с категорией удалит все её новости, а `PROTECT` не даст удалить категорию, пока на неё ссылаются новости (возникает `ProtectedError`).

6. **Для чего нужен `related_name`?** - Задаёт имя обратной связи. При `related_name='news'` новости категории доступны как `category.news.all()`.

7. **Чем отличаются `null=True` и `blank=True`?** - `null=True` разрешает хранить `NULL` в базе данных, а `blank=True` разрешает оставлять поле пустым при валидации формы.

8. **Почему нельзя просто указать `default=1` у внешнего ключа?** - Если в таблице категорий нет записи с `id=1`, нарушается ссылочная целостность и миграция завершается `IntegrityError`.

9. **Зачем нужен `db_index=True`?** - Создаёт индекс по полю и ускоряет поиск и сортировку по нему.

10. **Как сослаться на модель, объявленную ниже?** - Передать её имя строкой: `ForeignKey('Category', on_delete=models.PROTECT)`.

11. **Для чего нужен `__str__` в модели `Category`?** - Чтобы в выпадающем списке и в списке объектов админки выводилось название категории, а не `Category object (1)`.

12. **Как показать связанные данные и фильтры в админке?** - Добавить имя поля-связи в `list_display`, а для фильтра - в `list_filter`; `list_editable` позволяет менять поле прямо в списке.


## Рекомендуемые источники

1. **Официальная документация Django** - https://docs.djangoproject.com/
2. **Django: поля отношений** - https://docs.djangoproject.com/en/stable/ref/models/fields/#module-django.db.models.fields.related
3. **Django: связи между моделями** - https://docs.djangoproject.com/en/stable/topics/db/examples/many_to_one/
4. **Django: миграции** - https://docs.djangoproject.com/en/stable/topics/migrations/
5. **Django: административная панель** - https://docs.djangoproject.com/en/stable/ref/contrib/admin/
