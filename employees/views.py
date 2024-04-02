from datetime import date
from typing import Any
from django.shortcuts import render
from employees.models import fPonto, fPontoCorrecoes, dColaboradores
from employees.forms import fPontoForm
from django.views.generic import CreateView
from django.shortcuts import redirect
from django.contrib import messages
from django.utils.dateparse import parse_date

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
    
    form = fPontoForm(request.POST)
   
    if form.is_valid():

      # Definindo as variaveis usadas abaixo
      dateTime = form.cleaned_data['data']
      data = date(dateTime.year, dateTime.month, dateTime.day)
      colaborador = form.cleaned_data['idColaborador']
      
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
      elif action == 'corrigir':
        id_colaborador = request.POST.get('idColaborador')
        return redirect (f'/correcao/{id_colaborador}/{data}')
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
      return render(request, 'ponto_form.html', {'ponto_form': form})
  else:
    form = fPontoForm()
  return render(request, 'ponto_form.html', {'ponto_form': form})


def correcao(request, id_colaborador, data):
  form = fPontoCorrecoes(request.POST)

  # Criar listas de horas e minutos
  horas = ['{:02d}'.format(h) for h in range(6, 21)]
  minutos = ['{:02d}'.format(m) for m in range(60)]

  #Puxa nome do funcionario
  colaborador = dColaboradores.objects.get(idColaborador = id_colaborador)

  #Converte data para Date
  data_date = parse_date(data)
  
  return render(request, 'correcao_form.html', {'correcao_form': form, 'horas': horas, 'minutos': minutos, 'colaborador': colaborador, 'data': data_date})