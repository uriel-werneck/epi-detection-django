from functools import wraps
from django.shortcuts import redirect

def redirect_if_authenticated(func_view):
    @wraps(func_view)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard:home')
        return func_view(request, *args, **kwargs)
    return wrapper