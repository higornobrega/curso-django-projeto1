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
        add_placeholder(self.fields['password'], 'Type your password')
        add_placeholder(self.fields['password2'], 'Repeat your password')
        add_placeholder(self.fields['last_name'], 'Ex.: Nóbrega')
    
    
    # Sobrescrevendo o campos
    
    username = forms.CharField(
        label='username',
        help_text=(
            'Username must have letters, numbers or one of @.+-_. '
            'The length should be between 4 and 150 characters.'
        ),
        min_length=4, max_length=150,
    )
    
    password = forms.CharField(
        # required=True,
        widget=forms.PasswordInput(),
        error_messages={
            'required':'Password must not be empty'
        },
        help_text=(
            'Password must have at least one uppercase letter, '
            'one lowercase letter and one number. The lenght should be '
            'at least 8 characters.'
        ),
        validators=[strong_password],
        label='password',
        )
    
    # Criando campo extra 
    password2 = forms.CharField(
        # required=True, 
        error_messages={
            'required':'Please, repeat your password'
        },
        widget= forms.PasswordInput(),
        label='password2',

    )
    first_name = forms.CharField(
        error_messages={'required': 'Write your first name'},
        # required=True,
        label='First Name'
    )
    
    last_name = forms.CharField(
        error_messages={'required': 'Write your last name'},
        # required=True,
        label='last_name'
    )
    email = forms.EmailField(
        error_messages={'required': 'Write your e-mail'},
        # required=True,
        label='email',
        help_text = 'The e-mail must be valid',
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
        # labels = {
        #     'username': 'username',
        # }
        
        # Mensagem de ajuda abaixo do campo
             
        # Mensagem de erro
        error_messages = {
            'username':{
                'required': 'This field must not be empty', # Código do erro : mensagem do erro
            },
            'first_name':{
                'required': 'This field must not be empty', # Código do erro : mensagem do erro
            }
        }
        
        # Tipo e atributos para campo
        widgets = {
            'first_name':forms.TextInput(attrs={
                'class': 'input text-input'
            }),
        
        }
        
    # Validando Campos específicos
    # def clean_password(self):
    #     data = self.cleaned_data.get('password')
        
    #     if 'atenção' in data:
    #         raise ValidationError(
    #             'Não digite "atenção" no campo password',
    #             code='invalid',
    #             params={'value':'atenção'}
    #         )
        
    #     return data
    
    # Validando Campos específicos
    # def clean_first_name(self):
    #     data = self.cleaned_data.get('first_name')
        
    #     if 'John Doe' in data:
    #         raise ValidationError(
    #             'Não digite "John Doe" no campo first_name',
    #             code='invalid',
    #             params={'value':'John Doe'}
    #         )
        
    #     return data
    def clean_email(self):
        email = self.cleaned_data.get('email')
        user_exist = User.objects.filter(email=email).exists()
        if user_exist:
            raise ValidationError(
               'Email already exists' 
            )
        return email
            
    def clean(self) -> dict[str, Any]:
        cleaned_data = super().clean()
        
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        
        if password != password2:
            raise ValidationError({
                    'password':'Password and Password2 most be equals',
                    'password2':'Password and Password2 most be equals'
                })
        
