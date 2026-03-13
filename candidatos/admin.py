from django.contrib import admin
from .models import Candidato, ExameMedico, Psicologia, TesteFisico, Entrevista, Documento

class DocumentoInLine(admin.TabularInline):
    model = Documento
    extra = 3

class CandidatoAdmin(admin.ModelAdmin):
    inline = [DocumentoInLine]
    list_display = ('ra', 'nome', 'status')

admin.site.register(Candidato, CandidatoAdmin)
admin.site.register(ExameMedico)
admin.site.register(Psicologia)
admin.site.register(TesteFisico)
admin.site.register(Entrevista)
admin.site.register(Documento)