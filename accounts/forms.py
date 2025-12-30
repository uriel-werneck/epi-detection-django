from django.contrib.auth.forms import UserCreationForm
from .models import User

class UserRegisterForm(UserCreationForm):
    error_messages = {
        **UserCreationForm.error_messages,
        'password_mismatch': 'Senhas não coincidem!'
    }

    def clean_nome(self):
        cleaned_data = super().clean()
        nome = cleaned_data.get('nome')
        return nome.capitalize() if nome else nome

    def clean_sobrenome(self):
        sobrenome = self.cleaned_data.get('sobrenome')
        return sobrenome.capitalize() if sobrenome else sobrenome
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Já existe um usuário com esse email!')
        return email

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