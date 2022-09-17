from http.client import HTTPResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib import messages 
from .forms import SignUpForm, EditProfileForm
from scripts.parameters import main_proccess, retrieve_all_results
from scripts.record_audio import run_mike
from scripts.classes import record, start_recording, stop_recording, recorder, listener
from pynput.keyboard import Key, Controller
from scripts.calculate import calculation
import datetime

# from scripts.parameters import run_mike
date_str = datetime.datetime.now().timestamp()
date_str = str(datetime.datetime.now().timestamp())
date_str = date_str.split('.')
date_str = date_str[0] + date_str[1]
set_file_name = date_str
r = recorder(set_file_name + ".wav")
l = listener(r)
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
			messages.success(request, ('Error Logging In - Please Try Again...'))
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
			password = form.cleaned_data['password1']
			user = authenticate(username=username, password=password)
			login(request, user)
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
	return render(request, 'authenticate/estadisticas.html', {})

def estadisticas2(request):
	# call to backend with the results
	return render(request, 'authenticate/estadisticas2.html', {})

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

def record2(request):
	print('q to start recording, t to stop it')
	l.start()
	keyboard.press('q')
	l.join()
	# call to backend to retrieve last recorded audio
	gender, localShimmer, localJitter, f1_mean, f2_mean, hnr, total_evaluated_words = retrieve_all_results(set_file_name)
	print(gender, ' ', localShimmer, ' ', localJitter, ' ', f1_mean, ' ', f2_mean, ' ', hnr, ' ', total_evaluated_words)
	resulting_text, resulting_description = calculation(localJitter, localShimmer, f1_mean, f2_mean, hnr, gender, total_evaluated_words)
	print('last results')
	print('resulting_text ', resulting_text)
	print('resulting_num ', resulting_description)
	# insert into table of statistics resulting_text, resulting_description
	return redirect('estadisticas2')

def stop2(request):
	keyboard.press('t')
	l.join()
	context = {'form': 1, "process": "bri"}
	return render(request, 'authenticate/results.html', context)