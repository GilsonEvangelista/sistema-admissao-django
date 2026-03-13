from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from .models import Candidato

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

    total = Candidato.objects.count()
    analise = Candidato.objects.filter(status='ANALISE').count()
    apto = Candidato.objects.filter(status='APTO').count()
    inapto = Candidato.objects.filter(status='INAPTO').count()
    servir = Candidato.objects.filter(status='SERVIR').count()
    titular = Candidato.objects.filter(status='TITULAR').count()

    context = {
        'total': total,
        'analise': analise,
        'apto': apto,
        'inapto': inapto,
        'servir': servir,
        'titular': titular
    }

    return render(request, 'dashboard.html', context)