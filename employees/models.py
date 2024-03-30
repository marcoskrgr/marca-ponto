from django.db import models

class dColaboradores(models.Model):
    idColaborador = models.AutoField(primary_key=True)
    Nome = models.CharField(max_length=255, blank=False, null=False)
    cargoFuncao = models.CharField(max_length=255, blank=False, null=False)
    CPF = models.CharField(max_length=14, blank=True, null=True)
    tipoContrato = models.CharField(max_length=255, blank=True, null=True)
    endereco = models.CharField(max_length=255, blank=True, null=True)
    cep = models.CharField(max_length=8, blank=True, null=True)
    telefone = models.CharField(max_length=15, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    salario = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    custoMes = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    dtAdmissao = models.DateTimeField(blank=False, null=False)
    dtDemissaoAlteracao = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.Nome

class fPonto(models.Model):
    id = models.AutoField(primary_key=True)
    idColaborador = models.ForeignKey(dColaboradores, on_delete=models.CASCADE, related_name='ponto_colaborador')
    data = models.DateTimeField(blank=True, null=True)
    entrada = models.DateTimeField(blank=True, null=True)
    saidaIntervalo = models.DateTimeField(blank=True, null=True)
    entradaIntervalo = models.DateTimeField(blank=True, null=True)
    saida = models.DateTimeField(blank=True, null=True)
    saldoDiario = models.CharField(max_length=255, blank=True, null=True)
    justificado = models.BooleanField(default=False)
    entradaCorrecao = models.BooleanField(default=False)
    saidaIntervaloCorrecao = models.BooleanField(default=False)
    entradaIntervaloCorrecao = models.BooleanField(default=False)
    saidaCorrecao = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)


class fPontoCorrecoes(models.Model):
    idCorrecao = models.AutoField(primary_key=True)
    idColaborador = models.ForeignKey(dColaboradores, on_delete=models.CASCADE)
    data = models.DateTimeField(blank=False, null=False)
    horarioSubstituido = models.DateTimeField(blank=False, null=False)
    horario = models.DateTimeField(blank=False, null=False)

    def __str__(self):
        return f"{self.idColaborador} - {self.data}"