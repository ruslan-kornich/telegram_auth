from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import FormView
from django.contrib.auth.views import LogoutView
from django.shortcuts import render
from django.urls import reverse_lazy

from accounts.forms import UserForm
from accounts.models import Profile


def index(request):
    if request.user.is_authenticated:
        context = {
            'users': Profile.objects.filter(username=request.user.username)
        }
        return render(request, "accounts/index.html", context)
    else:
        return render(request, "accounts/login.html")


class TelegramLoginView(FormView):
    template_name = "accounts/login.html"
    form_class = UserForm
    success_url = reverse_lazy("index")

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(self.request, user)
        messages.success(
            self.request,
            f'Hi {self.request.POST["username"]}')
        return super().form_valid(form)


class TelegramLogoutView(LogoutView):
    def get_success_url(self):
        messages.success(self.request, 'Ви успішно вийшли')
        return reverse_lazy("index")
