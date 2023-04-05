from django.contrib import messages
from django.contrib.auth.views import FormView
from django.contrib.auth.views import LogoutView
from django.shortcuts import render
from django.urls import reverse_lazy

from accounts.forms import UserForm


def index(request):
    return render(request, "accounts/index.html")


class TelegramLoginView(FormView):
    template_name = "accounts/login.html"
    form_class = UserForm
    success_url = reverse_lazy("index")


class TelegramLogoutView(LogoutView):
    def get_success_url(self):
        messages.success(self.request, 'Ви успішно вийшли')
        return reverse_lazy("index")
