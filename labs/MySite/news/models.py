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
