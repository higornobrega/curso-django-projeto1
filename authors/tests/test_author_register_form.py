from django.test import TestCase
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
    def test_first_name_placeholder_is_correct(self, field, placeholder):
        form = RegisterForm()
        current_placeholder = form[field].field.widget.attrs['placeholder']
        
        self.assertEqual(placeholder, current_placeholder)