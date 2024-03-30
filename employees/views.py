from django.shortcuts import render


def employee_view(request):
    return render(request, 'employee.html')
