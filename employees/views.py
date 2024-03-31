from datetime import date
from typing import Any
from django.shortcuts import render
from employees.models import fPonto, dColaboradores
from employees.forms import fPontoForm
from django.views.generic import CreateView
from django.shortcuts import redirect
from django.contrib import messages

#Função para verificar se ja existe a data inserida para o colaborador inserido
def verificaData(ponto, colaborador, data):
  if not ponto:
    ponto = fPonto(idColaborador=colaborador, data=data)
    ponto.save()
    print("Depuração - Novo ponto criado:", ponto)
  else:
    print("Depuração - Ponto encontrado:", ponto)
  return ponto

def ponto_form(request):
  if request.method == 'POST':
    print(request.POST)
    form = fPontoForm(request.POST)
    if form.is_valid():

      # Definindo as variaveis usadas abaixo
      dateTime = form.cleaned_data['data']
      data = date(dateTime.year, dateTime.month, dateTime.day)
      colaborador = form.cleaned_data['idColaborador']
      campo_ponto = None

      #Verificando se ja existe o dia no ponto do funcionario
      ponto = fPonto.objects.filter(idColaborador=colaborador, data=data).first()
      ponto = verificaData(ponto, colaborador, data)

      # Verificar qual botão foi clicado
      action = request.POST.get('action')
      
       # Verifica se o campo correspondente já está preenchido
      if action == 'entrada' and ponto.entrada:
          messages.error(request, "O ponto de entrada já foi preenchido para este colaborador nesta data.")
      elif action == 'saidaIntervalo' and ponto.saidaIntervalo:
          messages.error(request, "O ponto de saída para intervalo já foi preenchido para este colaborador nesta data.")
      elif action == 'entradaIntervalo' and ponto.entradaIntervalo:
          messages.error(request, "O ponto de entrada do intervalo já foi preenchido para este colaborador nesta data.")
      elif action == 'saida' and ponto.saida:
          messages.error(request, "O ponto de saída já foi preenchido para este colaborador nesta data.")
      else:
        #Atualiza o campo do ponto correspondente
        if action == 'entrada':
          ponto.entrada = dateTime
        elif action == 'saidaIntervalo':
          ponto.saidaIntervalo = dateTime
        elif action == 'entradaIntervalo':
          ponto.entradaIntervalo = dateTime
        elif action == 'saida':
          ponto.saida = dateTime

        ponto.save() #Salva as alteracoes
        messages.success(request, 'Ponto cadastrado com sucesso!')

        return redirect('/ponto')
    else:
      # Retorno avisando que tem algo de errado
      return render(request, 'ponto_form.html', {'ponto_form': form})
  else:
    form = fPontoForm()
  return render(request, 'ponto_form.html', {'ponto_form': form})