from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from .models import Candidato, Documento
from .utils import importar_candidatos
import pandas as pd

def login_view(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/dashboard/')
        else:
            return render(request, 'login.html', {'erro':'Usuário ou senha inválidos'})

    return render(request,'login.html')

@login_required
def lista_candidatos(request):

    busca = request.GET.get('busca')

    if busca:
        candidatos_lista = Candidato.objects.filter(nome__icontains=busca) | Candidato.objects.filter(ra__icontains=busca)
    else:
        candidatos_lista = Candidato.objects.all()

    paginator = Paginator(candidatos_lista, 10)  # 10 por página
    page = request.GET.get('page')
    candidatos = paginator.get_page(page)

    context = {
        'candidatos': candidatos
    }

    return render(request, 'lista_candidatos.html', context)

@login_required
def ficha_candidato(request, candidato_id):
    candidato = get_object_or_404(Candidato, id=candidato_id)
    context = {
        'candidato': candidato
    }

    return render (request, 'ficha_candidato.html', context)

@login_required
def dashboard(request):

    total_candidatos = Candidato.objects.count()
    total_documentos = Documento.objects.count()

    # Exemplo simples de status
    candidatos_com_docs = Documento.objects.values("candidato").distinct().count()
    candidatos_pendentes = total_candidatos - candidatos_com_docs

    # Contagem por tipo de documento
    documentos_por_tipo = {}

    for doc in Documento.objects.all():
        documentos_por_tipo[doc.tipo] = documentos_por_tipo.get(doc.tipo, 0) + 1

    context = {
        "total_candidatos": total_candidatos,
        "total_documentos": total_documentos,
        "candidatos_com_docs": candidatos_com_docs,
        "candidatos_pendentes": candidatos_pendentes,
        "doc_labels": list(documentos_por_tipo.keys()),
        "doc_values": list(documentos_por_tipo.values()),
    }

    return render(request, "dashboard.html", context)

@login_required
def importar_excel(request):

    if request.method == "POST":

        arquivo = request.FILES["arquivo"]

        importar_candidatos(arquivo)

        return redirect("lista_candidatos")

    return render(request, "importar_excel.html")

def importar_planilha(request):

    df = pd.read_excel("caminho/da/sua_planilha.xlsx")

    total_linhas = 0
    total_importados = 0
    total_existentes = 0
    total_documentos = 0

    for _, row in df.iterrows():

        total_linhas += 1

        if pd.isna(row["CPF"]):
            continue

        cpf = str(row["CPF"])

        candidato, criado = Candidato.objects.get_or_create(
            cpf=cpf,
            defaults={
                "nome": row["NOME-COMPLETO"],
                "ra": row["RA"]
            }
        )

        if criado:
            total_importados += 1
        else:
            total_existentes += 1

        documentos = {
            "Situação Cadastral": row["ARQUIVO-SITUACAO-CADASTRAL (arquivo)"],
            "Certidão Nascimento": row["ARQUIVO-CERTIDAO-NASCIMENTO (arquivo)"],
            "RG": row["ARQUIVO-RG (arquivo)"],
            "Comprovante Endereço": row["ARQUIVO-ENDERECO (arquivo)"],
            "Histórico Escolar": row["ARQUIVO-ESCOLAR (arquivo)"],
            "CNH": row["ARQUIVO-CNH (arquivo)"],
            "Carteira Trabalho": row["ARQUIVO-CARTEIRA-TRABALHO (arquivo)"],
        }

        for tipo, link in documentos.items():

            if pd.notna(link):

                Documento.objects.create(
                    candidato=candidato,
                    tipo=tipo,
                    link=link
                )

                total_documentos += 1

    print("===== RELATÓRIO =====")
    print("Linhas:", total_linhas)
    print("Importados:", total_importados)
    print("Existentes:", total_existentes)
    print("Documentos:", total_documentos)

    return render(request, "importacao_sucesso.html", {
        "linhas": total_linhas,
        "importados": total_importados,
        "existentes": total_existentes,
        "documentos": total_documentos
    })