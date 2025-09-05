from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView

from auth_system.forms import CustomLoginForm, CustomUserCreationForm


# Create your views here.
class CustomLoginView(LoginView):
    template_name = "auth_system/login.html"
    redirect_authenticated_user = True
    form_class = CustomLoginForm

class CustomLogoutView(LogoutView):
    next_page = "login"

class RegisterView(CreateView):
    template_name = "auth_system/register.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("task-list")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)