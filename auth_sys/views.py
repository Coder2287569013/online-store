from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from .models import CustomUser
from .forms import CustomUserCreationForm

# Create your views here.
class CustomUserCreateView(CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'auth_sys/signup.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)

        return redirect('login')

class CustomLoginView(LoginView):
    template_name = 'auth_sys/login.html'