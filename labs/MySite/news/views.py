from django.http import HttpResponse


def index(request):
    return HttpResponse('Hello, world!')


def test(request):
    return HttpResponse('<h1>Тестовая страница</h1>')
