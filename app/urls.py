from django.contrib import admin
from django.urls import path
from employees.views import ponto_form, correcao

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ponto/', ponto_form, name='ponto_form'),
    path('correcao/<int:id_colaborador>/<str:data>/', correcao, name='correcao_form')
]
