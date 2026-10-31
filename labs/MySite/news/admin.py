from django.contrib import admin
from .models import News, Category, Topic, Message

# Register your models here.


class NewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'created_at',
                    'updated_at', 'is_published')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'content')
    list_editable = ('is_published',)
    list_filter = ('is_published', 'category')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    search_fields = ('title',)


class TopicAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'author_name', 'create_date', 'is_it_closed')
    search_fields = ('name',)


class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'topic', 'text', 'author_name', 'date', 'file')
    search_fields = ('text',)
    list_filter = ('date',)


admin.site.register(News, NewsAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.register(Message, MessageAdmin)
