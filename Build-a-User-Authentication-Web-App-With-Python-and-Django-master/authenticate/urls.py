from django.urls import path
from . import views

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
    path('results', views.get_voice_parameters, name='results'),
    path('record', views.record2, name='record'),
    path('stop', views.stop2, name='stop'),
]
