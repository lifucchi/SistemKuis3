from django.shortcuts import render

# Create your views here.

from django.shortcuts import render , redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm
from django.views.decorators.cache import never_cache
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.views.generic import CreateView
from django.urls import reverse_lazy

# Create your views here.
# def register(request, ):
#     if request.method == 'POST':
#         form = UserRegisterForm(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data.get('username')
#             messages.success(request, f'Akun sudah dibuat')
#             return redirect('login')
#
#     else:
#         form = UserRegisterForm()
#
#     return render(request, 'users/register.php' , {'form': form })

# Create your class.
class register(CreateView):
    form_class = UserRegisterForm
    success_url = reverse_lazy('login')
    template_name = 'users/register.php'



def login(request, **kwargs):
    if request.user.is_authenticated:
        return redirect('/home/')
    else:
        return auth_views.LoginView(request, **kwargs)