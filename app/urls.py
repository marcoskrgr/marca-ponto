from django.contrib import admin
from django.urls import path
from employees.views import ponto_form

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ponto/', ponto_form, name='ponto_form'),
]
