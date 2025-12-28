from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from .decorators import redirect_if_authenticated

# Create your views here.
@redirect_if_authenticated
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:login')
    else:
        form = UserRegisterForm()
        
    return render(request, 'accounts/register.html', {'form': form})
