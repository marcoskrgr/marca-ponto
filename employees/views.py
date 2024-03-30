from datetime import date
from typing import Any
from django.shortcuts import render
from employees.models import fPonto, dColaboradores
from employees.forms import fPontoForm
from django.views.generic import CreateView
from django.shortcuts import redirect
from django.contrib import messages

def ponto_form(request):
  if request.method == 'POST':
    form = fPontoForm(request.POST)
    if form.is_valid():
        dateTime = form.cleaned_data['data']
        data = date(dateTime.year, dateTime.month, dateTime.day)
        colaborador = form.cleaned_data['idColaborador']
        entrada = form.cleaned_data['entrada']

        ponto = fPonto.objects.filter(idColaborador=colaborador, data=data).first()

        if not ponto:
           ponto = fPonto(idColaborador=colaborador, data=data, entrada=entrada)
           ponto.save()
        elif not ponto.saidaIntervalo:
            saidaIntervalo = form.cleaned_data['saidaIntervalo']
            ponto.saidaIntervalo = saidaIntervalo
            ponto.save()
        elif not ponto.entradaIntervalo:
            entradaIntervalo = form.cleaned_data['entradaIntervalo']
            ponto.entradaIntervalo = entradaIntervalo
            ponto.save()
        elif not ponto.saida:
            saida = form.cleaned_data['saida']
            ponto.saida = saida
            ponto.save()
        else:
           ...
        return redirect('/ponto')
    else:
      # Handle form validation errors
      return render(request, 'ponto_form.html', {'ponto_form': form})
  else:
    form = fPontoForm()
  return render(request, 'ponto_form.html', {'ponto_form': form})



# def ponto_form(request):
#     form = fPontoForm()
#     return render(request, 'ponto_form.html', {'ponto_form' : form})
