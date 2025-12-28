from django.shortcuts import render
from accounts.decorators import redirect_if_authenticated

# Create your views here.
@redirect_if_authenticated
def index(request):
    return render(request, 'pages/index.html')