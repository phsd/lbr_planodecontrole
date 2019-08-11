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
from django.template.loader import render_to_string, get_template
from django.utils.text import slugify
from weasyprint import HTML, CSS
from weasyprint.fonts import FontConfiguration
from django.conf import settings
import os

from django.http import FileResponse, Http404

CONST_NUMTOTALINSPECOES = 2

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
    buscaItemInspecao = models.inspecaoPlanoControle.objects.raw(b)
    for b in buscaItemInspecao:
        print (b.id)
        print (b.numero)
    if (len(buscaItemInspecao) < CONST_NUMTOTALINSPECOES):
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
    inserir = models.inspecaoPlanoControle(id_HPC = hiddenidHPCSv, id_itemInspecaoPC = hiddenidItemInspecaoPCSv, serie = SerieSv, valor = valorSv, username_usuario = request.user.username, dataRegistro=datetime.datetime.now())
    inserir.save()
    inspecaoRegistrada = 'true'
    return render(request, 'telaPrincipal/inspecaoregistrada.json', {'inspecaoRegistrada': inspecaoRegistrada})

@login_required
def GerarPDFInspecoes(request):
    linhaMOSGerarPDF = []
    b = '''SELECT telaPrincipal_headerplanocontrole.id, telaPrincipal_headerplanocontrole.mo,
            telaPrincipal_headerplanocontrole.seriei, telaPrincipal_headerplanocontrole.serieii, telaPrincipal_headerplanocontrole.serieiii,
            telaPrincipal_inspecaoplanocontrole.serie, MAX(telaPrincipal_iteminspecaopc.numero) AS numeroInspecaoRealizada
        FROM
            telaPrincipal_headerplanocontrole
        LEFT JOIN
                telaPrincipal_inspecaoplanocontrole
        ON
                telaPrincipal_headerplanocontrole.id = telaPrincipal_inspecaoplanocontrole.id_HPC_id
        LEFT JOIN
                telaPrincipal_iteminspecaopc
        ON
                telaPrincipal_inspecaoplanocontrole.id_itemInspecaoPC_id = telaPrincipal_iteminspecaopc.id
        WHERE
                telaPrincipal_headerplanocontrole.pdfcriado = 0
        GROUP BY telaPrincipal_headerplanocontrole.id, telaPrincipal_inspecaoplanocontrole.serie
		ORDER BY telaPrincipal_headerplanocontrole.mo, telaPrincipal_inspecaoplanocontrole.serie;'''

    busca = models.inspecaoPlanoControle.objects.raw(b)

    if len(busca) > 0:
        ultimaMOEncontrada = busca[0].mo
        seriesdessaMO = [busca[0].seriei, busca[0].serieii, busca[0].serieiii]
        seriesEncontradasdessaMO = []
        mosGerarPDF = []
        btnGerarPDF = "true"

        for b in busca:
            if (b.mo != ultimaMOEncontrada):
                for i in range (0, 3):
                    if (not seriesdessaMO[i] in seriesEncontradasdessaMO):
                        mosGerarPDF.append([ultimaMOEncontrada, seriesdessaMO[i], 0, 0])
                        btnGerarPDF = "false"

                linhaMOSGerarPDF.append([mosGerarPDF[0][0], mosGerarPDF, btnGerarPDF])

                seriesdessaMO = [0, 0, 0]
                seriesEncontradasdessaMO = []
                mosGerarPDF = []
                btnGerarPDF = "true"


            if (not b.numeroInspecaoRealizada is None):
                mosGerarPDF.append([b.mo, b.serie, b.numeroInspecaoRealizada, round((b.numeroInspecaoRealizada/CONST_NUMTOTALINSPECOES)*100)])
                if (b.numeroInspecaoRealizada < CONST_NUMTOTALINSPECOES):
                    btnGerarPDF = "false"
                seriesdessaMO = [b.seriei, b.serieii, b.serieiii]
                seriesEncontradasdessaMO.append(b.serie)
                ultimaMOEncontrada = b.mo
            else:
                seriesdessaMO = [b.seriei, b.serieii, b.serieiii]
                seriesEncontradasdessaMO.append(b.serie)
                ultimaMOEncontrada = b.mo


        for i in range (0, 3):
            if (not seriesdessaMO[i] in seriesEncontradasdessaMO):
                mosGerarPDF.append([ultimaMOEncontrada, seriesdessaMO[i], 0, 0])
                btnGerarPDF = "false"

        linhaMOSGerarPDF.append([mosGerarPDF[0][0], mosGerarPDF, btnGerarPDF])

    contexto = {
        'linhaMOSGerarPDF': linhaMOSGerarPDF,
        'CONST_NUMTOTALINSPECOES': CONST_NUMTOTALINSPECOES
    }
    return render (request, "telaPrincipal/GerarPDFInspecoes.html", contexto)

@login_required
def BuscarPDFInspecoes(request):
    linhaMOSBuscarPDF = []
    b =  '''SELECT * FROM telaPrincipal_headerplanocontrole WHERE pdfcriado = 1;'''
    busca = models.inspecaoPlanoControle.objects.raw(b)
    for b in busca:
        linhaMOSBuscarPDF.append([b.mo, b.seriei, b.serieii, b.serieiii, b.datapdfcriado])
    contexto = {
        'busca': linhaMOSBuscarPDF,
    }
    return render (request, "telaPrincipal/BuscarPDFInspecoes.html", contexto)

def VisualizarPDFInspecoes(request, mo):
    dirname = os.path.dirname(__file__)
    response = FileResponse(open(dirname + '/../media/pdfs/'+ mo +'.pdf', 'rb'), content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename={title}.pdf'.format(title=mo)
    return response

def PDF_IPXX_XXX_19_2(request):
    html_template = get_template('telaPrincipal/PDF_IPXX_XXX_19.html')
    user = {
        'name': "nome",
        'address': "endereco"
    }
    rendered_html = html_template.render(user).encode(encoding="UTF-8")
    pdf_file = HTML(string=rendered_html).write_pdf(stylesheets=[CSS(os.path.dirname(__file__) +  '/static/css/report.css')])
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = 'filename="home_page.pdf"'
    return response

@login_required
def PDF_IPXX_XXX_19(request, mo):
    listInspecoesPCInformacoes = []
    listInspecoesPCSerieI = []
    listInspecoesPCSerieII = []
    listInspecoesPCSerieIII = []
    response = HttpResponse(content_type="application/pdf")
    nomeArquivo = "inline; filename=" + mo +".pdf"
    response['Content-Disposition'] = nomeArquivo.format()

    b =  '''SELECT * FROM telaPrincipal_headerplanocontrole WHERE mo = \''''+ mo + '''\';'''
    busca = models.inspecaoPlanoControle.objects.raw(b)
    b2 = '''SELECT
                telaPrincipal_inspecaoplanocontrole.id,
                telaPrincipal_iteminspecaopc.operacao, telaPrincipal_iteminspecaopc.numero, telaPrincipal_iteminspecaopc.cor,
            	telaPrincipal_iteminspecaopc.requisito, telaPrincipal_iteminspecaopc.ilustracao, telaPrincipal_iteminspecaopc.metodoinstrucao,
            	telaPrincipal_inspecaoplanocontrole.valor, telaPrincipal_inspecaoplanocontrole.username_usuario,
            	telaPrincipal_iteminspecaopc.unidade
            FROM
            	telaPrincipal_inspecaoplanocontrole
            INNER JOIN
            	telaPrincipal_iteminspecaopc
            ON
            	telaPrincipal_inspecaoplanocontrole.id_itemInspecaoPC_id = telaPrincipal_iteminspecaopc.id
            WHERE
                telaPrincipal_inspecaoplanocontrole.id_HPC_id = '''+ str(busca[0].id) +'''
            ORDER BY
                telaPrincipal_iteminspecaopc.numero;'''
    busca2 = models.inspecaoPlanoControle.objects.raw(b2)

    for b2 in busca2:
        if (b2.unidade == "OK/NOK"):
            unidade = ""
        else:
            unidade = b2.unidade
        if b2.serie == busca[0].seriei:
            listInspecoesPCInformacoes.append([b2.operacao, b2.numero, b2.cor, b2.requisito, b2.ilustracao, b2.metodoinstrucao])
            listInspecoesPCSerieI.append([b2.valor, b2.username_usuario, unidade])
        elif b2.serie == busca[0].serieii:
            listInspecoesPCSerieII.append([b2.valor, b2.username_usuario, unidade])
        elif b2.serie == busca[0].serieiii:
            listInspecoesPCSerieIII.append([b2.valor, b2.username_usuario, unidade])
    html = render_to_string("telaPrincipal/PDF_IPXX_XXX_19.html", {
        'headerPlanoControle': busca[0],
        'rgUsuario': request.user.username,
        'nomeUsuario': request.user.first_name,
        'listInspecoesPCInformacoes': listInspecoesPCInformacoes,
        'listInspecoesPCSerieI': listInspecoesPCSerieI,
        'listInspecoesPCSerieII': listInspecoesPCSerieII,
        'listInspecoesPCSerieIII': listInspecoesPCSerieIII
    })
    font_config = FontConfiguration()
    pdf_criado = HTML(string=html).write_pdf()
    dirname = os.path.dirname(__file__)
    if os.path.exists(dirname):
        with open(os.path.join(dirname, '../media/pdfs/'+ mo +'.pdf'), 'wb') as f:
            f.write(pdf_criado)
        atualizar = models.headerPlanoControle.objects.filter(id=busca[0].id).update(pdfcriado=True, datapdfcriado=datetime.datetime.now())

        response = FileResponse(open(dirname + '/../media/pdfs/'+ mo +'.pdf', 'rb'), content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename={title}.pdf'.format(title=mo)
        return response
