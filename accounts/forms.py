from django.contrib.auth.forms import UserCreationForm
from .models import User

class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'nome',
            'sobrenome',
            'telefone',
            'email',
            'password1',
            'password2'
        ]