from asyncio.windows_events import NULL
from http.client import HTTPResponse
from .models import *
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib import messages
from django.db.models import Avg
from .forms import SignUpForm, EditProfileForm
from scripts.parameters import main_proccess, retrieve_all_results
from scripts.classes import record, start_recording, stop_recording, recorder, listener
from pynput.keyboard import Key, Controller
from scripts.calculate import calculation
import datetime
from utils.constants import C_PATH
from rest_framework.views import APIView
from rest_framework.response import Response
import os

# from scripts.parameters import run_mike
keyboard = Controller()


def home(request):
    return render(request, 'authenticate/home.html', {})


def home_login(request):
    return render(request, 'authenticate/home_login.html', {})


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ('You Have Been Logged In!'))
            return redirect('home_login')

        else:
            messages.success(
                request, ('Error Logging In - Please Try Again...'))
            return redirect('login')
    else:
        return render(request, 'authenticate/login.html', {})


def logout_user(request):
    logout(request)
    messages.success(request, ('You Have Been Logged Out...'))
    return redirect('home')


def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)

            paciente = Paciente.objects.create(
                Paciente_Codigo=user.id,
                Paciente_Nombre=first_name,
                Paciente_Apellidos=last_name,
                Paciente_Usuario=username,
                Paciente_Edad=NULL,
                Paciente_Departamento=NULL,
                Paciente_Telefono=NULL,
                Paciente_DNI=NULL,
                Paciente_Correo=email,
                Paciente_Contrasena=password,
                Paciente_Rol=NULL,
            )

            formulario_titulo = ("formulario_"+username)
            formulario_detalle = ("Formulario asignado al usuario: "+username)

            formulario = Formulario.objects.create(
                Formulario_Titulo=formulario_titulo,
                Formulario_FechaCreacion=datetime.datetime.now(),
                Formulario_Detalle=formulario_detalle
            )

            encuesta_detalle = ("Encuesta asignada al usuario: "+username)

            encuesta = Encuesta.objects.create(
                Paciente_Paciente_Codigo=paciente,
                Formulario_Formulario_Codigo=formulario,
                Encuesta_FechaCompletado=datetime.datetime.now(),
                Encuesta_Detalle=encuesta_detalle
            )

            messages.success(request, ('You Have Registered...'))
            return redirect('home_login')
    else:
        form = SignUpForm()

    context = {'form': form}
    return render(request, 'authenticate/register.html', context)


def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, ('You Have Edited Your Profile...'))
            return redirect('home_login')
    else:
        form = EditProfileForm(instance=request.user)

    context = {'form': form}
    return render(request, 'authenticate/edit_profile.html', context)


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, ('You Have Edited Your Password...'))
            return redirect('home_login')
    else:
        form = PasswordChangeForm(user=request.user)

    context = {'form': form}
    return render(request, 'authenticate/change_password.html', context)


def estadisticas(request):
    paciente = Paciente.objects.get(Paciente_Codigo=request.user.id)
    encuesta = Encuesta.objects.get(
        Paciente_Paciente_Codigo=paciente.Paciente_Codigo)
    resultados = Resultado.objects.filter(Encuesta_Encuesta_Codigo=encuesta)
    promedio_parametros = resultados.aggregate(Avg('Resultado_por_parametros'))
    promedio_parametros = round(list(promedio_parametros.values())[0], 2)
    promedio_palabras = resultados.aggregate(Avg('Resultado_por_palabras_depresivas'))
    promedio_palabras = round(list(promedio_palabras.values())[0], 2)
    promedio_total = resultados.aggregate(Avg('Resultado_escala_total'))
    promedio_total = int(list(promedio_total.values())[0])
    return render(request, 'authenticate/estadisticas.html', 
    {"promedio_parametros": promedio_parametros,
    "promedio_palabras": promedio_palabras,
    "promedio_total": promedio_total})


def estadisticas2(request):
    # call to backend with the results
    paciente = Paciente.objects.get(Paciente_Codigo=request.user.id)
    encuesta = Encuesta.objects.get(
        Paciente_Paciente_Codigo=paciente.Paciente_Codigo)
    resultados = Resultado.objects.filter(
        Encuesta_Encuesta_Codigo=encuesta).order_by('-Resultado_Fecha')
    numero_resultados = len(list(resultados))
    return render(request, 'authenticate/estadisticas2.html', {"resultados": resultados, "numero_resultados": numero_resultados})


def historial(request):
    return render(request, 'authenticate/historial.html', {})


def reconocimiento(request):
    return render(request, 'authenticate/reconocimiento-1.html', {})


def reconocimiento2(request):
    return render(request, 'authenticate/reconocimiento-2.html', {})


def pendientes(request):
    return render(request, 'authenticate/pendientes.html', {})


def recomendaciones(request):
    return render(request, 'authenticate/recomendaciones.html', {})


def get_voice_parameters(request):
    context = {'form': 1, "process": main_proccess()}
    return render(request, 'authenticate/results.html', context)


def record_audio(request):
    start_recording()
    context = {'form': 1, "process": "bri"}
    return render(request, 'authenticate/results.html', context)


def stop_audio(request):
    stop_recording()
    context = {'form': 1, "process": "bri"}
    return render(request, 'authenticate/results.html', context)


def record_with_keys(request):
    record()
    context = {'form': 1, "process": "bri"}
    return render(request, 'authenticate/results.html', context)


def get_charts(request):
    return render(request, 'authenticate/charts.html')


def record2(request):
    date_str = datetime.datetime.now().timestamp()
    date_str = str(datetime.datetime.now().timestamp())
    date_str = date_str.split('.')
    date_str = date_str[0] + date_str[1]
    set_file_name = date_str
    print('set file name ', set_file_name)
    print('q to start recording, t to stop it')
    r = recorder(set_file_name + ".wav")
    l = listener(r)
    l.start()
    l.recorder.start()
    l.join()
    paciente = Paciente.objects.get(Paciente_Codigo=request.user.id)
    encuesta = Encuesta.objects.get(
        Paciente_Paciente_Codigo=paciente.Paciente_Codigo)
    gender, localShimmer, localJitter, f1_mean, f2_mean, hnr, total_evaluated_words = retrieve_all_results(
        set_file_name)
    print(gender, ' ', localShimmer, ' ', localJitter, ' ', f1_mean,
          ' ', f2_mean, ' ', hnr, ' ', total_evaluated_words)
    resulting_text, resulting_description,  calculated_result_parameters, quantity_depression_words, scale_by_parameters, scale_by_words_said, scale_final_result = calculation(
        localJitter, localShimmer, f1_mean, f2_mean, hnr, gender, total_evaluated_words)
    print('resulting_text ', resulting_text)
    print('resulting_num ', resulting_description)
    print('retrieved data ', resulting_text, 'desc ', resulting_description, 'numbers ', calculated_result_parameters, quantity_depression_words, scale_by_parameters, scale_by_words_said, scale_final_result)
    # call to backend to retrieve last recorded audio
    # insert into table of statistics resulting_text, resulting_description
    resultado = Resultado.objects.create(
        Encuesta_Encuesta_Codigo=encuesta,
        Resultado_Diagnostico=resulting_text,
        Resultado_Descripcion=resulting_description,
        Resultado_Recomendacion=NULL,
		Resultado_por_parametros = calculated_result_parameters,
		Resultado_por_palabras_depresivas = quantity_depression_words,
		Resultado_escala_total = scale_final_result,
		Resultado_escala_por_parametros = scale_by_parameters,
		Resultado_escala_por_palabras_depresivas = scale_by_words_said,
        Resultado_Fecha=datetime.datetime.now()
    )
    path1 = os.path.join(C_PATH, set_file_name+'.wav')
    path2 = os.path.join(C_PATH, set_file_name+'.TextGrid')
    os.remove(path1)
    os.remove(path2)
    return redirect('estadisticas2')


def stop2(request):
    keyboard.press('t')
    return redirect('estadisticas2')


class ChartData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        today = datetime.datetime.now()
        start_date = datetime.date(today.year, today.month, 1)
        end_date = datetime.date(today.year, today.month, 31)
        labels = ["Mínima", "Leve", "Moderada",
                  "Moderadamente severa", "Muy severa"]
        user_id = self.request.query_params.get('userId')
        paciente = Paciente.objects.get(Paciente_Codigo=user_id)
        encuesta = Encuesta.objects.get(
            Paciente_Paciente_Codigo=paciente.Paciente_Codigo)
        minimo = Resultado.objects.filter(
            Encuesta_Encuesta_Codigo=encuesta, Resultado_escala_total=1, Resultado_Fecha__range=(start_date, end_date)).count()
        leve = Resultado.objects.filter(
            Encuesta_Encuesta_Codigo=encuesta, Resultado_escala_total=2, Resultado_Fecha__range=(start_date, end_date)).count()
        moderada = Resultado.objects.filter(
            Encuesta_Encuesta_Codigo=encuesta, Resultado_escala_total=3, Resultado_Fecha__range=(start_date, end_date)).count()
        moderadamente_severa = Resultado.objects.filter(
            Encuesta_Encuesta_Codigo=encuesta, Resultado_escala_total=4, Resultado_Fecha__range=(start_date, end_date)).count()
        muy_severa = Resultado.objects.filter(
            Encuesta_Encuesta_Codigo=encuesta, Resultado_escala_total=5, Resultado_Fecha__range=(start_date, end_date)).count()
        total = Resultado.objects.filter(
            Encuesta_Encuesta_Codigo=encuesta, Resultado_Fecha__range=(start_date, end_date)).count()
        resultados_escala_total = Resultado.objects.filter(
            Encuesta_Encuesta_Codigo=encuesta).values_list('Resultado_escala_total', flat=True)
        
        resultados_escala_total = list(resultados_escala_total)

        fechas_de_todos_los_resultados = Resultado.objects.filter(
            Encuesta_Encuesta_Codigo=encuesta)
        fechas_de_todos_los_resultados = fechas_de_todos_los_resultados.extra(select={'datestr':"strftime( '%%Y-%%m-%%d %%H:%%M', Resultado_Fecha)"})
        fechas_de_todos_los_resultados = fechas_de_todos_los_resultados.values_list('datestr', flat=True)
        fechas_de_todos_los_resultados = list(fechas_de_todos_los_resultados)

        default_items = [minimo, leve, moderada,
                         moderadamente_severa, muy_severa]

        data = {
            "labels": labels,
            "default": default_items,
            "total": total,
            "fechas": fechas_de_todos_los_resultados,
            "resultados_totales": resultados_escala_total,
        }
        return Response(data)
