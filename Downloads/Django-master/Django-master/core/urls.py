# Importações necessárias para definir as rotas de URLs
from django.urls import path  # Importa a função path para definir as rotas de URL
from .views import home  # Importa a função de view 'home' do módulo 'views' local
from django.contrib.auth import views as auth_views  # Importa as views de autenticação do Django

from . import views

# Lista de padrões de URL para a aplicação 'core'
urlpatterns = [
    path('login/', views.login, name='login'),  # URL para a página de login
    path('', views.home, name='home'),          # URL para a home
    path('agendamento/', views.agendamento, name='agendamento'),
    path('servicos/', views.servicos, name='servicos'),
]
