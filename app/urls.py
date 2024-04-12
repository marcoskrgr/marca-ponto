from django.contrib import admin
from django.urls import path
from employees.views import ponto_form, correcao
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='/ponto/')),
    path('admin/', admin.site.urls),
    path('ponto/', ponto_form, name='ponto_form'),
    path('correcao/<int:id_colaborador>/<str:data>/', correcao, name='correcao_form')
]
