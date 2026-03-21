from django.db import models

class Candidato(models.Model):

    protocolo = models.CharField(max_length=50, blank=True)

    ra = models.CharField(max_length=20, blank=True, null=True)

    nome = models.CharField(max_length=200)

    cpf = models.CharField(max_length=11, unique=True)

    nome_mae = models.CharField(max_length=200, blank=True)

    nome_pai = models.CharField(max_length=200, blank=True)

    data_nascimento = models.DateField(null=True, blank=True)

    rg = models.CharField(max_length=20, blank=True)

    data_emissao_rg = models.DateField(null=True, blank=True)

    orgao_emissor_rg = models.CharField(max_length=50, blank=True)

    titulo_eleitor = models.CharField(max_length=20, blank=True)

    cnh = models.CharField(max_length=20, blank=True)

    estado_civil = models.CharField(max_length=20, blank=True)

    nivel_ensino = models.CharField(max_length=50, blank=True)

    telefone = models.CharField(max_length=20, blank=True)

    endereco = models.TextField(blank=True)

    email = models.EmailField(blank=True)

    experiencia_profissional = models.TextField(blank=True)

    deseja_servir = models.BooleanField(default=False)

    data_importacao = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    importado = models.BooleanField(default=False)

    STATUS_CANDIDATO = [
        ('ANALISE', 'Em análise'),
        ('APTO', 'Apto'),
        ('INAPTO', 'Inapto'),
        ('SERVIR', 'Quer servir'),
        ('TITULAR', 'Titular'),
    ]

    status = models.CharField(
        max_length=15, 
        choices=STATUS_CANDIDATO, 
        default='ANALISE'
        )

    def __str__(self):
        return f"{self.nome} - {self.cpf}"
    
    ETAPAS = [
    ("inscrito", "Inscrito"),
    ("documentos", "Documentos Aprovados"),
    ("psicologia", "Psicologia"),
    ("entrevista", "Entrevista"),
    ("tacf", "TACF"),
    ("medico", "Exame Médico"),
]

    etapa = models.CharField(
        max_length=20,
        choices=ETAPAS,
        default="inscrito"
)
    
def caminho_documento(instance, filename):
    return f'documentos/candidato_{instance.candidato.id}/{filename}'

class Documento(models.Model):

    candidato = models.ForeignKey('Candidato', on_delete=models.CASCADE, related_name='documentos')

    tipo = models.CharField(
        max_length=100,
    )

    link = models.URLField(blank=True, null=True)

    data_importacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.candidato.nome} - {self.tipo}"
    
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