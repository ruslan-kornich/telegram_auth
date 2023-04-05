from django.urls import path

from accounts.views import index, TelegramLoginView, TelegramLogoutView

urlpatterns = [
    path("", index, name="index"),
    path("login/", TelegramLoginView.as_view(), name="login"),
    path("logout/", TelegramLogoutView.as_view(), name="logout"),
]
