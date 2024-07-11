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
        ('username',(
            'Username must have letters, numbers or one of @.+-_. '
            'The length should be between 4 and 150 characters.'
        )),
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
        ('first_name','First Name'),
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
        ('username','Este campo é obrigatório.'),
        ('first_name','Write your first name'),
        ('last_name','Write your last name'),
        ('email','Write your e-mail'),        
        ('password','Password must not be empty'),        
        ('password2','Please, repeat your password'),        
        
    ])
    def test_fields_cannot_be_empty(self, field, msg):
        self.format_data[field] = ''
        url = reverse('authors:create')
        response = self.client.post(url, data=self.format_data, follow=True)
        # self.assertIn(msg, response.content.decode('utf-8'))       
        self.assertIn(msg, response.context['form'].errors.get(field))
        
    def test_username_field_min_length_should_be_4(self):
        self.format_data['username'] = 'joa'
        url = reverse('authors:create')
        response = self.client.post(url, data=self.format_data, follow=True)
        msg = f'Certifique-se de que o valor tenha no mínimo 4 caracteres (ele possui {len(self.format_data["username"])}).'
        self.assertIn(msg, response.context['form'].errors.get('username'))
        
    def test_username_field_max_length_should_be_150(self):
        self.format_data['username'] = 'i'*160
        url = reverse('authors:create')
        response = self.client.post(url, data=self.format_data, follow=True)
        msg = f'Certifique-se de que o valor tenha no máximo 150 caracteres (ele possui {len(self.format_data["username"])}).'
        self.assertIn(msg, response.context['form'].errors.get('username'))
        
    def test_password_field_have_lower_upper_case_letters_and_numbers(self):
        self.format_data['password'] = 'abcdefgji'
        url = reverse('authors:create')
        response = self.client.post(url, data=self.format_data, follow=True)
        msg = f'Password must have at least one uppercase letter, one lowercase letter and one number. The lenght should be at least 8 characters.'
        self.assertIn(msg, response.context['form'].errors.get('password'))
        
    def test_password_and_password_confirmation_are_equal(self):
        self.format_data['password'] = 'abc123@A'
        self.format_data['password2'] = 'abc123@'
        url = reverse('authors:create')
        response = self.client.post(url, data=self.format_data, follow=True)
        msg = f'Password and Password2 most be equals'
        self.assertIn(msg, response.context['form'].errors.get('password'))
        
        
    def test_send_get_request_to_registration_create_view_returns_404(self):
        url = reverse('authors:create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        
        
    def test_send_post_correct(self):
        url = reverse('authors:create')
        response = self.client.post(url, data=self.format_data, follow=True)
        self.assertEqual(response.status_code, 200)
        
    def test_email_alrealy_exist(self):
        url = reverse('authors:create')
        self.client.post(url, data=self.format_data, follow=True)
        response = self.client.post(url, data=self.format_data, follow=True)
        msg = f'Email already exists'
        self.assertIn(msg, response.context['form'].errors.get('email'))
        
    def test_author_created_can_login(self):
        url = reverse('authors:create')
        self.format_data.update({
            'username':'testuser',
            'password':'@123abcABC',
            'password2':'@123abcABC',
        })
        self.client.post(url, data=self.format_data, follow=True)
        
        is_authenticated = self.client.login(
            username='testuser',
            password='@123abcABC'
        )
        self.assertTrue(is_authenticated)
