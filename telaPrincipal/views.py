from django.shortcuts import render
from datetime import datetime, timedelta, timezone, date
import datetime
import calendar
from . import models
import pytz
import math
from django.contrib import messages
import calendar

from django.http import HttpResponseRedirect
from django.urls import reverse

from django.contrib.auth.decorators import login_required

from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils.text import slugify
from weasyprint import HTML
from weasyprint.fonts import FontConfiguration
import os

from django.http import FileResponse, Http404

# Create your views here.
@login_required
def index(request):
    contexto = {
    }
    return render (request, "telaPrincipal/index.html", contexto)

def carregarMO(request):
    MOBuscar = request.GET.get('MOBuscar')
    b = '''SELECT
                *
        FROM
            telaPrincipal_headerplanocontrole
        WHERE
            mo = \''''+ MOBuscar +'''\';'''
    buscaMO = models.headerPlanoControle.objects.raw(b)
    return render(request, 'telaPrincipal/carregarMO.json', {'buscaMO': buscaMO})

def carregarItemInspecao(request):
    MOBuscar = request.GET.get('MOBuscar')
    SerieBuscar = request.GET.get('SerieBuscar')
    finalizado = 'false'
    compermissao = 'false'
    proximoItem = []
    b = '''SELECT telaPrincipal_inspecaoplanocontrole.id, telaPrincipal_iteminspecaopc.numero FROM telaPrincipal_inspecaoplanocontrole
        INNER JOIN
        	telaPrincipal_headerplanocontrole
        ON
        	telaPrincipal_inspecaoplanocontrole.id_HPC_id = telaPrincipal_headerplanocontrole.id
        INNER JOIN
        	telaPrincipal_iteminspecaopc
        ON
        	telaPrincipal_inspecaoplanocontrole.id_itemInspecaoPC_id = telaPrincipal_iteminspecaopc.id
        AND
        	telaPrincipal_inspecaoplanocontrole.serie = ''' + SerieBuscar + '''
        AND
        	telaPrincipal_headerplanocontrole.mo = \'''' + MOBuscar + '''\'
        ORDER BY
        	telaPrincipal_iteminspecaopc.numero DESC;'''
    print(b)
    buscaItemInspecao = models.inspecaoPlanoControle.objects.raw(b)
    if (len(buscaItemInspecao) < 3):
        if (len(buscaItemInspecao) == 0):
            numeroProximaInspecao = 1
        else:
            numeroProximaInspecao = buscaItemInspecao[0].numero + 1
        c = 'SELECT * FROM telaPrincipal_iteminspecaopc WHERE numero = ' + str(numeroProximaInspecao) + ';'
        proximoItem = models.itemInspecaoPC.objects.raw(c)
        compermissao = 'true'
    else:
        finalizado = 'true'
    return render(request, 'telaPrincipal/carregarItemInspecao.json', {'finalizado': finalizado, 'compermissao': compermissao, 'proximoItem': proximoItem})

def registrarInspecao(request):
    inspecaoRegistrada = 'false'
    SerieSv = request.GET.get('SerieSv')
    valorSv = request.GET.get('valorSv')
    hiddenidHPCSv = request.GET.get('hiddenidHPCSv')
    hiddenidItemInspecaoPCSv = request.GET.get('hiddenidItemInspecaoPCSv')
    for d in models.headerPlanoControle.objects.filter(id = hiddenidHPCSv):
        hiddenidHPCSv = d
    for e in models.itemInspecaoPC.objects.filter(id = hiddenidItemInspecaoPCSv):
        hiddenidItemInspecaoPCSv = e
    inserir = models.inspecaoPlanoControle(id_HPC = hiddenidHPCSv, id_itemInspecaoPC = hiddenidItemInspecaoPCSv, serie = SerieSv, valor = valorSv, id_usuario = request.user.id, dataRegistro=datetime.datetime.now())
    inserir.save()
    inspecaoRegistrada = 'true'
    return render(request, 'telaPrincipal/inspecaoregistrada.json', {'inspecaoRegistrada': inspecaoRegistrada})

def PDF_IPXX_XXX_19(request):
    variavel = "valor da variavel"
    response = HttpResponse(content_type="application/pdf")
    response['Content-Disposition'] = "inline; filename=mypdf.pdf".format()
    html = render_to_string("telaPrincipal/PDF_IPXX_XXX_19.html", {
        'variavel': variavel,
    })

    font_config = FontConfiguration()
    pdf_criado = HTML(string=html).write_pdf()
    dirname = os.path.dirname(__file__)
    if os.path.exists(dirname):
        with open(os.path.join(dirname, 'static/pdfs/mypdf.pdf'), 'wb') as f:
            f.write(pdf_criado)
            response = FileResponse(open(dirname + '/static/pdfs/mypdf.pdf', 'rb'), content_type='application/pdf')
            response['Content-Disposition'] = 'inline; filename={title}.pdf'.format(
                title="titulo")
            return response

def PDF_IPXX_XXX_19_2(request):
    variavel = "aqui esta é a variavel"
    response = HttpResponse(content_type="application/pdf")
    response['Content-Disposition'] = "inline; filename=donation-receipt.pdf"
    html = render_to_string("telaPrincipal/PDF_IPXX_XXX_19.html", {
        'variavel': variavel,
    })

    font_config = FontConfiguration()
    HTML(string=html).write_pdf(response, font_config=font_config)
    return response
