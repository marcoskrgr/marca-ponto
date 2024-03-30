from django.contrib import admin
from employees.models import dColaboradores, fPonto

class ColaboradorAdmin(admin.ModelAdmin):
    list_display = ('idColaborador', 'Nome', 'cargoFuncao', 'CPF', 'telefone', 'dtAdmissao')
    search_fields = ('Nome',)

admin.site.register(dColaboradores, ColaboradorAdmin)

class PontoAdmin(admin.ModelAdmin):
    list_display = ('id', 'idColaborador', 'data', 'entrada', 'saidaIntervalo', 'entradaIntervalo', 'saida', 'saldoDiario', 'justificado', 'entradaCorrecao', 'saidaIntervaloCorrecao', 'entradaIntervaloCorrecao', 'saidaCorrecao' )
    list_filter = ('idColaborador', 'data',)

admin.site.register(fPonto, PontoAdmin)

