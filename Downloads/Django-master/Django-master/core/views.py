from django.shortcuts import render
from django.contrib.auth.decorators import login_required  # Importa o decorador login_required
 # Protege a view home para que apenas usuários autenticados possam acessá-la
def home(request):
    return render(request, 'core/home.html')  # Renderiza o template home.html

def login(request):
    return render(request, 'core/login.html')  

def agendamento(request):
    return render(request, 'core/agendamento.html')

def servicos(request):
    return render(request, 'core/servicos.html')

## Carrossel
from django.shortcuts import render

def carousel_view(request):
    reviews = [
        {"text": "Ótimo serviço!", "author": "Ana Silva"},
        {"text": "Excelente atendimento!", "author": "João Souza"},
        {"text": "Recomendo muito!", "author": "Maria Pereira"},
        {"text": "Equipe muito profissional!", "author": "Carlos Oliveira"},
        {"text": "Nota 10!", "author": "Fernanda Lima"},
    ]
    
    return render(request, 'carousel.html', {'reviews': reviews})
