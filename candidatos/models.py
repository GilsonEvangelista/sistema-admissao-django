from django.db import models

class Candidato(models.Model):
    ra = models.IntegerField(unique=True)
    nome = models.CharField(max_length=200)
    solucao = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.nome
    
class ExameMedico(models.Model):

    candidato = models.ForeignKey(Candidato, on_delete=models.CASCADE)

    data_exame_f1 = models.DateField(null=True, blank=True)
    resultado_f1 = models.CharField(max_length=50, null=True, blank=True)
    cid_f1 = models.CharField(max_length=20, null=True, blank=True)

    data_exame_f2 = models.DateField(null=True, blank=True)
    resultado_f2 = models.CharField(max_length=50, null=True, blank=True)
    cid_f2 = models.CharField(max_length=20, null=True, blank=True)

    parecer = models.TextField(null=True, blank=True)
    observacoes = models.TextField(null=True, blank=True)

class Psicologia(models.Model):
    candidato = models.ForeignKey(Candidato, on_delete=models.CASCADE)

    data_ex1 = models.DateField(null=True, blank=True)
    res_apto = models.BooleanField(default=False)

class TesteFisico(models.Model):

    candidato = models.ForeignKey(Candidato, on_delete=models.CASCADE)

    data_teste = models.DateField(null=True, blank=True)

    flexao = models.IntegerField(null=True, blank=True)
    abdominal = models.IntegerField(null=True, blank=True)
    corrida = models.FloatField(null=True, blank=True)

    nota_final = models.FloatField(null=True, blank=True)

    resultado = models.CharField(max_length=50, null=True, blank=True)

class Entrevista(models.Model):

    candidato = models.ForeignKey(Candidato, on_delete=models.CASCADE)

    periodo = models.CharField(max_length=20, null=True, blank=True)

    consideracoes = models.TextField(null=True, blank=True)

    resultado = models.CharField(max_length=50, null=True, blank=True)

    ivj_social = models.CharField(max_length=100, null=True, blank=True)

    entrevistador = models.CharField(max_length=200, null=True, blank=True)