from typing import Any
from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.db.models import Q
from django.views import generic
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.contrib import messages
from . import GetDataframe
from .GetDataframe import carga_general_db
import imgkit
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm
from django.conf import settings
import os
import tempfile
from weasyprint import HTML
from weasyprint.text.fonts import FontConfiguration
from django.template.loader import render_to_string, get_template
import datetime
import zoneinfo
import re
from unicodedata import normalize
from .models import DatosPersonales, Disc, TrabajoEquipo, Liderazgo
from .forms import DatosPersonalesForm
import base64

zona_asuncion = zoneinfo.ZoneInfo("America/Asuncion")

def _jinja2_filter_datetime(date, fmt=None):
    if isinstance(date, datetime.datetime):
        native = date.replace(tzinfo=None)
    elif isinstance(date, datetime.date):
        native = datetime.datetime(date.year, date.month, date.day)
    else:
        return date # Retorna el valor original si no es una fecha/hora

    if fmt:
        return native.strftime(fmt)
    else:
        return native.strftime('%d/%m/%Y') # Formato por defecto si no se especifica

# Create your views here.
class Home(LoginRequiredMixin, generic.TemplateView):
    login_url='base:login'
    def get(self, request):
        global df_dcl
        df_dcl = GetDataframe.cargar_dataframe()
        total = GetDataframe.df_info_inicial(df_dcl)
        columns = total.columns.values
        dict_total = total.to_dict('records')
        return render(request, 'base/disctotal.html', locals())

def custom_404(request, exception):
    return render(request, 'error/404.html', status=404)

def custom_500(request):
    return render(request, 'error/500.html', status=500)


class DatosPersonalesListView(LoginRequiredMixin, generic.ListView):
    model = DatosPersonales
    template_name = 'base/datos_personales_list.html'
    context_object_name = 'datos_personales'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(nombre__icontains=query) |
                Q(apellido__icontains=query) |
                Q(cedula__icontains=query) |
                Q(email__icontains=query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        return context


class DatosPersonalesUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = DatosPersonales
    form_class = DatosPersonalesForm
    template_name = 'base/datos_personales_form.html'
    success_url = '/datos-personales/'


class TestCompletoList(LoginRequiredMixin, generic.ListView):
    template_name = 'base/test_completo_list.html'
    context_object_name = 'tests_completados'
    paginate_by = 10

    def get_queryset(self):
        queryset = Disc.objects.select_related('aplicante').values(
            'campo_unico', 'fc',
            'aplicante__nombre', 'aplicante__apellido', 'aplicante__cedula', 'aplicante__email',
            'aplicante__fechaNacimiento', 'aplicante__edad', 'aplicante__celular'
        ).order_by('-fc')

        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(aplicante__nombre__icontains=query) |
                Q(aplicante__apellido__icontains=query) |
                Q(aplicante__cedula__icontains=query) |
                Q(aplicante__email__icontains=query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        return context

class DiscTotal(LoginRequiredMixin, generic.TemplateView):
    def get(self, request):
        df_dcl = GetDataframe.cargar_dataframe()
        total = GetDataframe.df_info_inicial(df_dcl)
        columns = total.columns.values
        dict_total = total.to_dict('records')
        return render(request, 'base/disctotal.html', locals())



class ResultadoTest(LoginRequiredMixin,generic.TemplateView):
    template_name = 'base/resultado_test_dcl.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        campo_unico = self.kwargs['val']
        data = carga_general_db(campo_unico)
        info = data['df_total']
        info.columns = info.columns.str.replace(" ", "_")
        context['df_aplicado'] = info.iloc[0].to_dict()
        context['graf_disc'] = data['graf_disc']
        context['graf_care'] = data['graf_care']
        context['graf_lider'] = data['graf_lider']
        context['care_list'] = data['care_list']
        context['campo_unico'] = campo_unico
        return context

class ResultadoDisc(LoginRequiredMixin, generic.TemplateView):
    def get(self, request, val):
        val_int = int(val)
        #val_int -= 1
        df_disc = GetDataframe.cargar_dataframe()
        df_disc1 = df_disc.iloc[[val_int]]
        total = GetDataframe.carga_total_completo(val_int)
        graf_disc = GetDataframe.get_disc_graf(val_int, df_disc1)
        graf_care = GetDataframe.get_grafico_polar_care_render(val_int, df_disc1)
        graf_lider = GetDataframe.get_grafico_polar_liderazgo_render(val_int, df_disc1)
        care_list = GetDataframe.list_care_for_graf(val_int, df_disc1)
        total_ = total.iloc[:,10:14].T
        disc_list_pc = total_[0].values.tolist()
        
        total.columns = total.columns.str.replace(" ", "_")
        
        dict_total = total.to_dict('records')
        nombre = dict_total[0]['Nombre_y_Apellido'].replace(' ', '-')
        nombre = re.sub(r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+",
                r"\1", normalize("NFD", nombre),0,re.I)
        #valor_url = request.build_absolute_uri(reverse('base:grafico_care', args=[val_int]))
       
        """ con = imgkit.config(wkhtmltoimage='C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltoimage.exe')
        imgkit.from_url(valor_url , 'out.png', config=con) """
        return render(request, 'base/informedisc.html', locals())

class TestDcl(generic.TemplateView):
    def get(self, request):
        return render(request, 'base/testdcl.html')

class TestDclInterno(generic.TemplateView):
    def get(self, request):
        return render(request, 'base/testdcl_in.html')

class RegistroTest(generic.TemplateView):
    def get(self, request):
        return render(request, 'base/registro_test.html')

class ViewGraficoCare(generic.TemplateView):
    def get(self, request, val):
        val_int = int(val)
        total = GetDataframe.carga_total_completo(val_int)
        total.columns = total.columns.str.replace(" ", "_")
        care_list = GetDataframe.list_care_for_graf(val_int)
        dict_total = total.to_dict('records')
        return render(request, 'base/informediscCare.html', locals())
    

class DescargarWordDB(generic.TemplateView):
    def get(self, request, val):
        hora_asuncion = datetime.datetime.now(zona_asuncion)
        hora_asuncion = hora_asuncion.strftime('%d/%m/%Y')
        
        data = carga_general_db(val)
        info = data['df_total']
        namefile = f"{info.iloc[0]['nombre']} {info.iloc[0]['apellido']}"
        info.columns = info.columns.str.replace(" ", "_")

        dict_total = info.to_dict('records')
        dict_total_fin = dict_total[0]

        if isinstance(dict_total_fin['fechaNacimiento'], str):
            try:
                # Asume formato 'YYYY-MM-DD' si es un string
                dict_total_fin['fechaNacimiento'] = datetime.datetime.strptime(dict_total_fin['fechaNacimiento'], '%Y-%m-%d').date()
            except ValueError:
                # Manejar el error si el formato del string no es el esperado
                print(f"Fecha no registrada: {dict_total_fin['fechaNacimiento']}") # O loggear el error, o asignar un valor por defecto

        # Formatea la fecha a 'd/m/yyyy' antes de pasarla al contexto
        if isinstance(dict_total_fin['fechaNacimiento'], (datetime.date, datetime.datetime)):
            dict_total_fin['fechaNacimiento_formateada'] = dict_total_fin['fechaNacimiento'].strftime('%d/%m/%Y')
        else:
            dict_total_fin['fechaNacimiento_formateada'] = "Fecha no disponible" # O un valor por defecto

        response = HttpResponse(content_type='application/msword')
        response['Content-Disposition'] = f'attachment; filename="{namefile}.docx"'
        
        path_plantilla = os.path.join(settings.BASE_DIR,'base', 'plantilla', 'Plantilla_Informe6.docx') 
        doc = DocxTemplate(path_plantilla)
        # graficos
        imagen_disc = base64.b64decode(data['graf_disc'])
        imagen_care = base64.b64decode(data['graf_care'])
        imagen_lider = base64.b64decode(data['graf_lider'])
        fp = tempfile.NamedTemporaryFile()
        with open(f"{fp.name}.png", 'wb') as temp_file:
            temp_file.write(imagen_care)
            img_temp = str(temp_file.name)
            imagen = InlineImage(doc, img_temp, width=Mm(90), height=Mm(85))
        fp2 = tempfile.NamedTemporaryFile()
        with open(f"{fp2.name}.png", 'wb') as temp_file2:
            temp_file2.write(imagen_lider)
            img_temp = str(temp_file2.name)
            imagen2 = InlineImage(doc, img_temp, width=Mm(90) )
        fp3 = tempfile.NamedTemporaryFile()
        with open(f"{fp3.name}.png", 'wb') as temp_file3:
            temp_file3.write(imagen_disc)
            img_temp = str(temp_file3.name)
            imagen3 = InlineImage(doc, img_temp, width=Mm(60))
        nombre = f"{request.user.first_name} {request.user.last_name}"
        context = {'imagen': imagen, 'dict_total_fin': dict_total_fin, 'imagen2': imagen2, 'imagen3': imagen3, 'hora':hora_asuncion, 'user': nombre}
        doc.render(context)
        doc.save(response)
        return response

class DescargarWord(generic.TemplateView):
    def get(self, request, val):
        val_int = int(val)
        hora_asuncion = datetime.datetime.now(zona_asuncion)
        hora_asuncion = hora_asuncion.strftime('%d/%m/%Y')
        #info_test = GetDataframe.info_test_total(val_int)
        df_disc = GetDataframe.cargar_dataframe()
        df_disc1 = df_disc.iloc[[val_int]]
        #Dict info total DCL
        total = GetDataframe.carga_total_completo(val_int)
        graf_care = GetDataframe.get_grafico_polar_care_word(val_int, df_disc1)
        graf_lider = GetDataframe.get_grafico_polar_liderazgo_word(val_int, df_disc1)
        graf_disc = GetDataframe.get_disc_word(val_int, df_disc1)
        name = total['Nombre y Apellido'].values.tolist()
        total.columns = total.columns.str.replace(" ", "_")
        dict_total = total.to_dict('records')
        dict_total_fin = dict_total[0]
        response = HttpResponse(content_type='application/msword')
        response['Content-Disposition'] = f'attachment; filename="{name[0]}.docx"'
        
        path_plantilla = os.path.join(settings.BASE_DIR,'base', 'plantilla', 'Plantilla_Informe4.docx') 
        doc = DocxTemplate(path_plantilla)
        
        fp = tempfile.NamedTemporaryFile()
        with open(f"{fp.name}.png", 'wb') as temp_file:
            temp_file.write(graf_care)
            img_temp = str(temp_file.name)
            imagen = InlineImage(doc, img_temp, width=Mm(90), height=Mm(85))
        fp2 = tempfile.NamedTemporaryFile()
        with open(f"{fp2.name}.png", 'wb') as temp_file2:
            temp_file2.write(graf_lider)
            img_temp = str(temp_file2.name)
            imagen2 = InlineImage(doc, img_temp, width=Mm(90) )
        fp3 = tempfile.NamedTemporaryFile()
        with open(f"{fp3.name}.png", 'wb') as temp_file3:
            temp_file3.write(graf_disc)
            img_temp = str(temp_file3.name)
            imagen3 = InlineImage(doc, img_temp, width=Mm(60))
        nombre = f"{request.user.first_name} {request.user.last_name}"
        context = {'imagen': imagen, 'dict_total_fin': dict_total_fin, 'imagen2': imagen2, 'imagen3': imagen3, 'hora':hora_asuncion, 'user': nombre}
        doc.render(context)
        doc.save(response)
        return response
    

class DescargarPdfAlt(generic.TemplateView):
    def get(self, request, name, val):
        val_int = int(val)
        info_test = GetDataframe.info_test_total(val_int)
        nombres= info_test['Nombre y Apellido'].values.tolist()
        #Dict info total DCL
        total = GetDataframe.carga_total_completo(val_int)
        total.columns = total.columns.str.replace(" ", "_")
        dict_total = total.to_dict('records')
        dict_total_fin = dict_total[0]
        graf_disc = GetDataframe.get_disc_graf(val_int)
        graf_care = GetDataframe.get_grafico_polar_care_render(val_int)
        graf_lider = GetDataframe.get_grafico_polar_liderazgo_render(val_int)
        context = {'dict_total':dict_total,
                   'graf_disc':graf_disc,
                   'graf_care':graf_care,
                   'graf_lider':graf_lider,
                   'name':nombres[0]}
        html = render_to_string("base/informepdf.html", context)

        response = HttpResponse(content_type="application/pdf")
        
        font_config = FontConfiguration()
        html = HTML(string=html)
        result = html.write_pdf(encoding='utf-8',font_config=font_config, filename=f'{name}.pdf')
        response["Content-Disposition"] = f'attachment; filename:"{name}.pdf"'
        response.write(result)
        return response
    
def enviarMail(request):
    if request.method == 'POST':
        nameid = request.POST['user_id']
        name = request.POST['name']
        val_int = int(nameid)
        valor_url = request.build_absolute_uri(reverse('base:informepdfalt_dcl', args=[val_int]))
        context = {'name':name,
                   'valor_url':valor_url}
        template = render_to_string("base/template_email.html", context)
        asunto = f"Resultados informe de {name}"
        mail = EmailMessage(
            asunto,
            template,
            settings.EMAIL_HOST_USER,
            ['deltadare@gmail.com']
        )
        mail.fail_silently = False
        mail.attach(f'{name}.pdf', create_pdf(val_int), 'application/pdf')
        mail.send()
        messages.success(request, 'Se ha enviado el correo')
        val_int += 1
        return redirect('base:informe_disc', val=val_int)
    
def create_pdf(val):

    val_int = int(val)
    info_test = GetDataframe.info_test_total(val_int)
    name = info_test['Nombre y Apellido'].values.tolist()
    #Dict info total DCL
    total = GetDataframe.carga_total_completo(val_int)
    total.columns = total.columns.str.replace(" ", "_")
    dict_total = total.to_dict('records')
    dict_total_fin = dict_total[0]
    graf_disc = GetDataframe.get_disc_graf(val_int)
    graf_care = GetDataframe.get_grafico_polar_care_render(val_int)
    graf_lider = GetDataframe.get_grafico_polar_liderazgo_render(val_int)
    context = {'dict_total':dict_total,
                   'graf_disc':graf_disc,
                   'graf_care':graf_care,
                   'graf_lider':graf_lider,
                   'name':name[0]}
    template_name = 'base/informepdf.html'
    template = get_template(template_name)
    html = template.render(context)
    font_config = FontConfiguration()
    pdf_binary = HTML(string=html).write_pdf(font_config=font_config)

    return pdf_binary