from django.shortcuts import render, redirect
from django.views.generic import View
from datetime import datetime, date
from django.contrib import messages
from jinja2.utils import F
from .models import DatosPersonales, Disc, TrabajoEquipo, Liderazgo
import uuid

class FormularioTestView(View):
    def get(self, request):
        return render(request, 'base/formulario_test.html')
    
    def post(self, request):
        # Obtener datos personales
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        email = request.POST.get('email')
        telefono = request.POST.get('telefono')
        cedula = request.POST.get('cedula')
        fechaNacimiento = request.POST.get('fecha_nacimiento')
        nacionalidad = request.POST.get('nacionalidad')
        estadoCivil = request.POST.get('estado_civil')
        print(fechaNacimiento)
        # Calcular la edad a partir de la fecha de nacimiento
        if fechaNacimiento:
            try:
                # Asumiendo formato YYYY-MM-DD
                fecha_nacimiento_obj = datetime.strptime(fechaNacimiento, '%Y-%m-%d').date()
                today = date.today()
                edad = today.year - fecha_nacimiento_obj.year - ((today.month, today.day) < (fecha_nacimiento_obj.month, fecha_nacimiento_obj.day))
            except ValueError:
                edad = None  # O manejar el error como prefieras
        else:
            edad = None
        # Obtener respuestas de los ítems
        respuestas = {}
        for i in range(1, 57):
            respuesta = request.POST.get(f'item{i}')
            respuestas[f'item{i}'] = respuesta
        for i in range(1, 13):
            for j in range(1, 5):
                if f'care{i}_{j}' in request.POST:
                    respuestas[f'care{i}_{j}'] = request.POST[f'care{i}_{j}']
        for i in range(1, 13):
            for j in range(1, 6):        
                if f'liderazgo{i}_{j}' in request.POST:
                    respuestas[f'liderazgo{i}_{j}'] = request.POST[f'liderazgo{i}_{j}']
        # Aquí se puede procesar las respuestas, guardarlas en la base de datos, etc.
        # Por ahora, solo mostraremos un mensaje de éxito
        obj, created = DatosPersonales.objects.update_or_create(
            cedula=cedula,
            defaults={
            'nombre':nombre,
            'apellido':apellido,
            'fechaNacimiento':fechaNacimiento,
            'nacionalidad':nacionalidad,
            'estadoCivil':estadoCivil,
            'email':email,
            'celular':telefono,
            'edad':edad
            }   
        )
        campo_unico = uuid.uuid4()
        disc = Disc(aplicante=obj, campo_unico=campo_unico)
        trabajo_equipo = TrabajoEquipo(aplicante=obj, campo_unico=campo_unico)
        #trabajo_equipo.save()
        options = ['a', 'b', 'c', 'd', 'e']	
        liderazgo = Liderazgo(aplicante=obj, campo_unico=campo_unico)
        #liderazgo.save()
        for i in range(1, 57):
            setattr(disc, f'item_{i}', respuestas[f'item{i}'])
        for i in range(1, 13):
            for j in range(1, 5):
                setattr(trabajo_equipo, f'item{i}{options[j-1]}', respuestas[f'care{i}_{j}'])
        for i in range(1, 13):
            for j in range(1, 6):
                setattr(liderazgo, f'item{i}{options[j-1]}', respuestas[f'liderazgo{i}_{j}'])
        disc.save()
        trabajo_equipo.save()
        liderazgo.save()
        messages.info(request, 'Formulario ya enviado anteriormente.')
        #datos_personales.save()
        messages.success(request, 'Formulario enviado correctamente. ¡Gracias por participar!')
        return redirect('base:registro_test')  # Redirigir a la página principal
