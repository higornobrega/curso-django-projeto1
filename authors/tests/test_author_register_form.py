from unittest import TestCase

from django.test import TestCase as DjangoTestCase
from django.urls import reverse
from parameterized import parameterized

from authors.forms import RegisterForm


class AuthorsRegisterFormUnitTest(TestCase):
    
    @parameterized.expand([
        ('email','Your Email'),
        ('username','Your username'),
        ('first_name','Ex.: Higor'),
        ('password','Type your password'),
        ('password2','Repeat your password'),
        ('last_name','Ex.: Nóbrega'),
    ])
    def test_fields_placeholder(self, field, placeholder):
        form = RegisterForm()
        current_placeholder = form[field].field.widget.attrs['placeholder']
        
        self.assertEqual(placeholder, current_placeholder)
    
    
    @parameterized.expand([
        ('username','Obrigatório. 150 caracteres ou menos. Letras, números e @/./+/-/_ apenas.'),
        ('email','The e-mail must be valid'),
        ('password',('Password must have at least one uppercase letter, '
            'one lowercase letter and one number. The lenght should be '
            'at least 8 characters.')) 
    ])
    def test_fields_help_text(self, field, needed):
        form = RegisterForm()
        current = form[field].field.help_text
        
        self.assertEqual(current, needed )
        
    @parameterized.expand([
        ('first_name','first_name'),
        ('last_name','last_name'),
        ('username','username'),
        ('email','email'),
        ('password','password'),
        ('password2','password2'),
    ])
    def test_fields_label(self, field, needed):
        form = RegisterForm()
        current = form[field].field.label
        
        self.assertEqual(current, needed )
        
class AuthorsRegisterFormIntegrationTest(DjangoTestCase):
    def setUp(self, *args, **kwargs) -> None:
        self.format_data = {
            'username': 'user',
            'first_name': 'first',
            'last_name': 'last',
            'email': 'email@anyemail.com',
            'password':'Str0ngP@ssword1',
            'password2':'Str0ngP@ssword1',
        }
        
        return super().setUp(*args, **kwargs)

    @parameterized.expand([
        ('username','This field must not be empty'),
    ])
    def test_fields_cannot_be_empty(self, field, msg):
        self.format_data[field] = ''
        url = reverse('authors:create')
        response = self.client.post(url, data=self.format_data, follow=True)
        self.assertIn(msg, response.content.decode('utf-8'))