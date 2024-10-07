from django import forms
from .models import Usuario

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nome', 'cpf', 'celular', 'date', 'email', 'sexo']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }
class LoginForm(forms.Form):
    email = forms.EmailField(label='Email')
    cpf = forms.CharField(label='CPF', max_length=11)
    