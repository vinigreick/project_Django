from django.contrib import admin
from django.urls import path, include
from core import views  # Importando as views do 'core'

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Definir a home como a página principal
    path('', views.home, name='home'),

    # URL para acessar a página de login
    path('login/', views.login, name='login'),

    path('accounts/', include('django.contrib.auth.urls')),

    # Incluir todas as URLs do app 'core'
    path('home/', include('core.urls')),
]
