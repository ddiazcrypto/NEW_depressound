from django.urls import path
from . import views
from .views import ChartData

urlpatterns = [
    path('', views.home, name="home"),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('change_password', views.change_password, name='change_password'),
    path('home_login', views.home_login, name='home_login'),
    path('estadisticas', views.estadisticas, name='estadisticas'),
    path('estadisticas2', views.estadisticas2, name='estadisticas2'),
    path('historial', views.historial, name='historial'),
    path('reconocimiento', views.reconocimiento, name='reconocimiento'),
    path('reconocimiento2', views.reconocimiento2, name='reconocimiento2'),
    path('pendientes', views.pendientes, name='pendientes'),
    path('recomendaciones', views.recomendaciones, name='recomendaciones'),
    path('charts', views.get_charts, name='charts'),
    path('results', views.get_voice_parameters, name='results'),
    path('record', views.record2, name='record'),
    path('stop', views.stop2, name='stop'),
    path('stop_last', views.stop_last, name='stop_last'),
    path('first_question', views.first_question, name='first_question'),
    path('second_question', views.second_question, name='second_question'),
    path('end_form', views.end_form, name='end_form'),
    path('third_question', views.third_question, name='third_question'),
    path('stop_first_question', views.stop_first_question, name='stop_first_question'),
    path('stop_second_question', views.stop_second_question, name='stop_second_question'),
    path('api/chart/data/', ChartData.as_view()),

]
