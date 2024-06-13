from django import forms
from django.contrib.auth.models import User


class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        # Campos a serem exibidos
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
        ]
        
        # Campos a serem excluídos
        # exclude = ['first_name'] 
        
        # Titulo que mostra a cima do campo 
        labels = {
            'first_name': 'first_name',
            'last_name': 'last_name',
            'username': 'username',
            'email': 'email',
            'password': 'password',
        }
        
        # Mensagem de ajuda abaixo do campo
        help_texts = {
            'email':'The e-mail must be valid',
        }
        
        # Mensagem de erro
        error_messages = {
            'username':{
                'required': 'This field must not be empty', # Código do erro : mensagem do erro
            }
        }
        
        # Tipo e atributos para campo
        widgets = {
            'first_name':forms.TextInput(attrs={
                'placeholder':'Type your username here',
                'class': 'input text-input'
            }),
            'password': forms.PasswordInput(attrs={
                    'placeholder': 'Type your password here'
            })
        }