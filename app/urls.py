from django.contrib import admin
from django.urls import path
from employees.views import employee_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ponto/', employee_view)
]
