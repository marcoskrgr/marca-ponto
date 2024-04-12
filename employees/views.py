from datetime import date, datetime, timedelta
from django.shortcuts import render, redirect
from employees.models import fPonto, fPontoCorrecoes, dColaboradores
from employees.forms import fPontoForm
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.utils import timezone

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
  id_colaborador = request.GET.get('idColaborador')
  pontos_do_colaborador = []
  colaborador = None  # Inicializa a variável colaborador

  if id_colaborador:
    colaborador = get_object_or_404(dColaboradores, pk=id_colaborador)
    data_atual = datetime.now().date()
    pontos_do_colaborador = fPonto.objects.filter(idColaborador=colaborador, data=data_atual)

  # Verificar se há algum ponto não marcado no dia anterior
  if colaborador:  # Verifica se colaborador está definido
    data_anterior = timezone.now().date() - timedelta(days=1)
    ponto_anterior = fPonto.objects.filter(idColaborador=colaborador, data=data_anterior).first()
    if ponto_anterior:
      if not ponto_anterior.entrada or not ponto_anterior.saidaIntervalo or not ponto_anterior.entradaIntervalo or not ponto_anterior.saida:
        messages.warning(request, "Você não pode marcar novos pontos até corrigir o ponto pendente do dia anterior.")
        return redirect('/ponto')  # Redireciona para evitar bater novos pontos
        
  form = fPontoForm(request.POST)

  if request.method == 'POST':
    if 'btn_buscar_pontos' in request.POST:
      id_colaborador = request.POST.get('idColaborador')
      colaborador = get_object_or_404(dColaboradores, pk=id_colaborador)
      data_atual = datetime.now().date()
      pontos_do_colaborador = fPonto.objects.filter(idColaborador=colaborador, data=data_atual)
    else:
        # Verificar se é sábado ou domingo (fim de semana)
        data_atual = datetime.now().date()
        if data_atual.weekday() in [5, 6]:  # 5 é sábado, 6 é domingo
          messages.info(request, "Fim de semana! Não é necessário marcar ponto.")
          return redirect('/ponto')  # Redireciona para evitar bater pontos no fim de semana
      
        # Verificar se há algum ponto não marcado no dia anterior
        data_anterior = timezone.now().date() - timedelta(days=1)
        ponto_anterior = fPonto.objects.filter(idColaborador=colaborador, data=data_anterior).first()
        if ponto_anterior:
          if not ponto_anterior.entrada or not ponto_anterior.saidaIntervalo or not ponto_anterior.entradaIntervalo or not ponto_anterior.saida:
            messages.warning(request, "Você não pode marcar novos pontos até corrigir o ponto pendente do dia anterior.")
            return redirect('/ponto')  # Redireciona para evitar bater novos pontos
        
        form = fPontoForm(request.POST)
        if form.is_valid():
          # Definindo as variáveis usadas abaixo
          dateTime = form.cleaned_data['data']
          data = date(dateTime.year, dateTime.month, dateTime.day)  # Combine a data com a hora mínima
          
          # Colaborador
          colaborador = form.cleaned_data['idColaborador']
          
          # Verificando se já existe o dia no ponto do funcionário
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
            # Atualiza o campo do ponto correspondente
            if action == 'entrada':
              ponto.entrada = dateTime
              print(ponto.entrada)
            elif action == 'saidaIntervalo':
              ponto.saidaIntervalo = dateTime
              print(ponto.saidaIntervalo)
            elif action == 'entradaIntervalo':
              ponto.entradaIntervalo = dateTime
              print(ponto.entradaIntervalo)
            elif action == 'saida':
              ponto.saida = dateTime
              print(ponto.saida)

            ponto.save() # Salva as alterações
            messages.success(request, 'Ponto cadastrado com sucesso!')
            return redirect('/ponto')
        else:
          return render(request, 'ponto_form.html', {'ponto_form': form})
  else:
    form = fPontoForm()
  return render(request, 'ponto_form.html', {'ponto_form': form, 'pontos_do_colaborador': pontos_do_colaborador})


def correcao(request, id_colaborador, data):
  form = fPontoCorrecoes(request.POST)

  # Obter a data do ponto a partir da URL
  data_ponto = datetime.strptime(data, '%Y-%m-%d')

  # Obter o colaborador
  colaborador = dColaboradores.objects.get(idColaborador=id_colaborador)

  # Verificar se o método da requisição é POST
  if request.method == 'POST':
    
    # Obter os dados do formulário
    tipo_ponto = request.POST.get('dropdownPonto')
    hora = int(request.POST.get('hora'))
    minuto = int(request.POST.get('minuto'))


    # Obter o objeto fPonto correspondente à data e ao colaborador
    ponto = fPonto.objects.get(idColaborador=colaborador, data=data_ponto)

    #Criando a variavel que vai receber o horario original do ponto
    horario_original = None
    
    # Marcar o campo correspondente do fPontoCorrecoes
    if tipo_ponto == 'entrada':
        horario_original = ponto.entrada
        print(horario_original)
        ponto.entrada = ponto.entrada.replace(hour=hora, minute=minuto)
        print(ponto.entrada)
        ponto.entradaCorrecao = True
    elif tipo_ponto == 'saidaIntervalo':
        horario_original = ponto.saidaIntervalo
        ponto.saidaIntervalo = ponto.saidaIntervalo.replace(hour=hora, minute=minuto)
        ponto.saidaIntervaloCorrecao = True
    elif tipo_ponto == 'entradaIntervalo':
        horario_original = ponto.entradaIntervalo
        ponto.entradaIntervalo = ponto.entradaIntervalo.replace(hour=hora, minute=minuto)
        ponto.entradaIntervaloCorrecao = True
    elif tipo_ponto == 'saida':
        horario_original = ponto.saida
        ponto.saida = ponto.saida.replace(hour=hora, minute=minuto)
        ponto.saidaCorrecao = True
        
    # Salvar as alterações no objeto fPonto
    ponto.save()

    # Criar uma instância de fPontoCorrecoes
    fPontoCorrecoes.objects.create(
        idColaborador=colaborador,
        data=data_ponto,
        horarioSubstituido=data_ponto.replace(hour=hora, minute=minuto),  
        horario=horario_original.strftime('%Y-%m-%d %H:%M:%S'), # Substituir pelo horário original do ponto
    )

    # Salvar as alterações no objeto fPonto
    ponto.save()

    # Adicionar mensagem de sucesso
    messages.success(request, 'Ponto corrigido com sucesso!')
  
  # Criar listas de horas e minutos
  horas = ['{:02d}'.format(h) for h in range(6, 21)]
  minutos = ['{:02d}'.format(m) for m in range(60)]

  return render(request, 'correcao_form.html', {'correcao_form': form, 'horas': horas, 'minutos': minutos, 'colaborador': colaborador, 'data': data})