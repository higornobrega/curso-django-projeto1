import re
from typing import Any

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


def strong_password(password):
    regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$')
    if not regex.match(password):
        raise ValidationError((
            'Password must have at least one uppercase letter, '
            'one lowercase letter and one number. The lenght should be '
            'at least 8 characters.'
        ),
            code='Invalid'
        )

def add_attr(field, attr_name, attr_new_val):
    existing_attr = field.widget.attrs.get(attr_name, '')
    field.widget.attrs[attr_name] = f'{existing_attr} {attr_new_val}'.strip()

def add_placeholder(field, placeholder_val):
    add_attr(field, 'placeholder', placeholder_val)
class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_attr(self.fields['email'], 'placeholder', 'Your Email')
        add_placeholder(self.fields['username'], 'Your username')
        add_placeholder(self.fields['first_name'], 'Ex.: Higor')
        add_placeholder(self.fields['last_name'], 'Ex.: Nóbrega')
        add_attr(self.fields['username'], 'css', 'a-css-class')
    
    
    # Sobrescrevendo o campos
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder':'Your passwor'
            }
        ),
        error_messages={
            'required':'Password must not be empty'
        },
        help_text=(
            'Password must have at least one uppercase letter, '
            'one lowercase letter and one number. The lenght should be '
            'at least 8 characters.'
        ),
        validators=[strong_password]
    )
    
    # Criando campo extra 
    password2 = forms.CharField(
        required=True, 
        widget=forms.PasswordInput(attrs={
            'placeholder':'Repeat your password'                            
        })
    )
    
    
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
        
    # Validando Campos específicos
    def clean_password(self):
        data = self.cleaned_data.get('password')
        
        if 'atenção' in data:
            raise ValidationError(
                'Não digite "atenção" no campo password',
                code='invalid',
                params={'value':'atenção'}
            )
        
        return data
    
    # Validando Campos específicos
    def clean_first_name(self):
        data = self.cleaned_data.get('first_name')
        
        if 'John Doe' in data:
            raise ValidationError(
                'Não digite "John Doe" no campo first_name',
                code='invalid',
                params={'value':'John Doe'}
            )
        
        return data
    
    def clean(self) -> dict[str, Any]:
        cleaned_data = super().clean()
        
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        
        if password != password2:
            raise ValidationError({
                    'password':'Password and Password2 most be equals',
                    'password2':'Password and Password2 most be equals'
                })
        
