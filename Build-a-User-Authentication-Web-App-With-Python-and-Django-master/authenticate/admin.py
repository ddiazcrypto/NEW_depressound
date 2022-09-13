from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Usuario)
admin.site.register(Paciente)
admin.site.register(Formulario)
admin.site.register(Encuesta)
admin.site.register(Resultado)
admin.site.register(Tipo_Pregunta)
admin.site.register(Pregunta)
admin.site.register(Encuesta_X_Pregunta)