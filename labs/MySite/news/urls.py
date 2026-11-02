from django.urls import path
from .views import index, test, test2

urlpatterns = [
    path('', index),
    path('test/', test),
    path('test/test2/', test2),
]
