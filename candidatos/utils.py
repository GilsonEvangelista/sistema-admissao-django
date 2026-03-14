import openpyxl
from .models import Candidato

def importar_candidatos(arquivo):

    workbook = openpyxl.load_workbook(arquivo)
    sheet = workbook.active

    for row in sheet.iter_rows(min_row=2):

        ra = row[0].value
        nome = row[1].value

        Candidato.objects.get_or_create(
            ra=ra,
            defaults={
                "nome": nome
            }
        )
