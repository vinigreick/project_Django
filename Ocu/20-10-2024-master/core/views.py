from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from .models import Cadastro, Agendamento
# View para a página inicial (home)
def home(request):
    return render(request, 'core/home.html')
    

def recepcao_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if user.groups.filter(name='Recepção').exists():
                login(request, user)
                return redirect('recepcao_dashboard')  # Redireciona para o dashboard da recepção
            else:
                messages.error(request, "Você não tem permissão para acessar esta área.")
        else:
            messages.error(request, "Usuário ou senha inválidos.")
    
    return render(request, 'core/login_recepcao.html')

@login_required
def recepcao_dashboard(request):
    if not request.user.groups.filter(name='Recepção').exists():
        return redirect('recepcao_login')

    agendamentos = Agendamento.objects.all().order_by('data')

    # Capturar os parâmetros de filtro do formulário
    data = request.GET.get('data', '').strip()
    cliente = request.GET.get('cliente', '').strip()
    status = request.GET.get('status', '').strip()
    servico = request.GET.get('servico', '').strip()
    periodo = request.GET.get('periodo', '').strip()

    # Aplicar os filtros de forma cumulativa, ignorando valores vazios
    if data:
        agendamentos = agendamentos.filter(data=data)
    if cliente:
        agendamentos = agendamentos.filter(cliente__nome__icontains=cliente)
    if status:
        agendamentos = agendamentos.filter(status=status)
    if servico:
        agendamentos = agendamentos.filter(servico__icontains=servico)
    if periodo:
        agendamentos = agendamentos.filter(periodo=periodo)

    return render(request, 'core/recepcao_dashboard.html', {'agendamentos': agendamentos})

# View para a página de login
def login_cliente(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        lembrar = request.POST.get('lembrar')

        try:
            usuario = Cadastro.objects.get(email=email)
            if usuario.check_password(senha):
                # Armazena os dados do usuário na sessão
                request.session['usuario_id'] = usuario.id
                request.session['usuario_nome'] = usuario.nome
                request.session['usuario_cpf'] = usuario.cpf
                request.session['usuario_email'] = usuario.email

                # Define o tempo de expiração da sessão com base no checkbox "lembrar"
                if lembrar:
                    request.session.set_expiry(60 * 60 * 24 * 30)  # 30 dias
                else:
                    request.session.set_expiry(0)  # Sessão expira ao fechar o navegador

                return redirect('home')
            else:
                messages.error(request, "Email ou senha incorretos. Tente novamente.")
        except Cadastro.DoesNotExist:
            messages.error(request, "Email ou senha incorretos. Tente novamente.")

    return render(request, 'core/login.html')

# View para a página de logout
def logout(request):
    auth_logout(request)  # Limpa a sessão e faz o logout
    return redirect('login')  # Redireciona o usuário para a página de login após sair

# View para o agendamento, acessível apenas para usuários logados
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Agendamento, Cadastro

def agendamento(request):
    if 'usuario_id' not in request.session:
        return redirect('login')  # Redireciona para login se o usuário não estiver logado

    usuario_id = request.session['usuario_id']
    usuario = Cadastro.objects.get(id=usuario_id)

    if request.method == 'POST':
        nome = request.POST.get('nom')
        cpf = request.POST.get('cpf')
        telefone = request.POST.get('tel')
        email = request.POST.get('email')
        data = request.POST.get('data')
        servico = request.POST.get('médico')
        periodo = request.POST.get('periodo')
        convenio = request.POST.get('convênio')
        detalhes_extras = request.POST.get('des')

        # Cria um novo agendamento
        agendamento = Agendamento(
            cliente=usuario,  # Passa a instância do usuário autenticado
            nome=nome,
            cpf=cpf,
            telefone=telefone,
            email=email,
            data=data,
            servico=servico,
            periodo=periodo,
            convenio=convenio,
            detalhes_extras=detalhes_extras
        )
        agendamento.save()
        return redirect('agendamento')

    
    agendamentos = Agendamento.objects.filter(cliente=usuario)
    
    agendamentos = Agendamento.objects.filter(cliente=usuario).order_by('data')  # Ordena pela data mais próxima
    return render(request, 'core/agendamento.html', {'agendamentos': agendamentos})


def exames(request):
    return render(request, 'core/exames.html')

def cirurgias(request):
    return render(request, 'core/cirurgias.html')

def usuarios(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        cpf = request.POST.get('cpf')
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        try:
            if Cadastro.objects.filter(email=email).exists():
                messages.error(request, "Um usuário com este e-mail já está cadastrado.")
                return redirect('login')
            elif Cadastro.objects.filter(nome=nome).exists():
                messages.error(request, "Um usuário com este nome já está cadastrado.")
                return redirect('login')
            elif Cadastro.objects.filter(cpf=cpf).exists():
                messages.error(request, "Um usuário com este CPF já está cadastrado.")
                return redirect('login')
            else:
                novo_usuario = Cadastro(nome=nome, cpf=cpf, email=email)
                novo_usuario.set_password(senha)  # Armazena a senha de forma segura
                novo_usuario.save()
                return redirect('login')
        except IntegrityError as e:
            messages.error(request, str(e))

    usuarios = {
        'usuarios': Cadastro.objects.all(),
    }

    return render(request, 'core/usuarios.html', usuarios)

def cadastrar(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        cpf = request.POST.get('cpf')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        
        novo_usuario = Cadastro(nome=nome, cpf=cpf, email=email)
        novo_usuario.set_password(senha)  # Armazena a senha de forma segura
        novo_usuario.save()
        
        return redirect('login')  # Redireciona para a página de login  
    
def servicos(request):
    return render(request, 'servicos.html')

from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Agendamento  # Certifique-se de que você importou o modelo corretamente

def alterar_status(request, agendamento_id, novo_status):
    # Obtém o agendamento ou retorna 404 se não encontrado
    agendamento = get_object_or_404(Agendamento, id=agendamento_id)
    
    # Opcional: Verifique se novo_status é válido
    status_permitidos = ['Pendente', 'Confirmado', 'Remarcado', 'Recusado']
    if novo_status not in status_permitidos:
        messages.error(request, 'Status inválido!')
        return redirect('home')  # Redireciona em caso de status inválido
    
    # Atualiza o status do agendamento
    agendamento.status = novo_status
    agendamento.save()
    
    # Mensagem de sucesso
    messages.success(request, 'Status atualizado com sucesso!')
    
    return redirect('recepcao_dashboard') 