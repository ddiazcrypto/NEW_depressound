from django.db import models

# Create your models here.

class Paciente(models.Model):
    Paciente_Codigo = models.PositiveIntegerField(primary_key=True)
    Paciente_Nombre = models.CharField(max_length=40)
    Paciente_Apellidos = models.CharField(max_length=40)
    Paciente_Edad = models.CharField(max_length=2)
    Paciente_Departamento = models.CharField(max_length=40)
    Paciente_Telefono = models.CharField(max_length=9)
    Paciente_DNI = models.CharField(max_length=8)
    Paciente_Correo = models.CharField(max_length=40, default='-')
    Paciente_Contrasena = models.CharField(max_length=40, default='-')
    Paciente_Rol = models.CharField(max_length=40, default='-')

class Formulario(models.Model):
    Formulario_Codigo = models.PositiveIntegerField(primary_key=True)
    Formulario_Titulo = models.CharField(max_length=40)
    Formulario_FechaCreacion = models.DateField()
    Formulario_Detalle = models.CharField(max_length=100)

class Encuesta(models.Model):
    Encuesta_Codigo = models.PositiveIntegerField(primary_key=True)
    Paciente_Paciente_Codigo = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    Formulario_Formulario_Codigo = models.ForeignKey(Formulario, on_delete=models.CASCADE)
    Encuesta_FechaCompletado = models.DateField()
    Encuesta_Detalle = models.CharField(max_length=100)

class Resultado(models.Model):
    Resultado_Codigo = models.PositiveIntegerField(primary_key=True)
    Encuesta_Encuesta_Codigo = models.ForeignKey(Encuesta, on_delete=models.CASCADE)
    Resultado_Diagnostico = models.CharField(max_length=80)
    Resultado_Descripcion = models.CharField(max_length=200)
    Resultado_Recomendacion = models.CharField(max_length=140)
    Resultado_Fecha = models.DateField()

class Tipo_Pregunta(models.Model):
    TipoPregunta_Codigo = models.PositiveIntegerField(primary_key=True)
    TipoPregunta_Descripcion = models.CharField(max_length=40)

class Pregunta(models.Model):
    Pregunta_Codigo = models.PositiveIntegerField(primary_key=True)
    Pregunta_Interrogante = models.CharField(max_length=80)
    Pregunta_Nivel = models.CharField(max_length=40)
    Tipo_Pregunta_TipoPregunta_Codigo = models.ForeignKey(Tipo_Pregunta, on_delete=models.CASCADE)
    

class Encuesta_X_Pregunta(models.Model):
    EncuestaPregunta_Codigo = models.PositiveIntegerField(primary_key=True)
    Formulario_Formulario_Codigo = models.ForeignKey(Formulario, on_delete=models.CASCADE)
    Pregunta_Pregunta_Codigo = models.ForeignKey(Pregunta, on_delete=models.CASCADE)