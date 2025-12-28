from django.contrib.auth.forms import UserCreationForm
from .models import User

class UserRegisterForm(UserCreationForm):
    def clean_nome(self):
        cleaned_data = super().clean()
        nome = cleaned_data.get('nome')
        return nome.capitalize() if nome else nome

    def clean_sobrenome(self):
        sobrenome = self.cleaned_data.get('sobrenome')
        return sobrenome.capitalize() if sobrenome else sobrenome

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