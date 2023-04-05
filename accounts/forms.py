from django.contrib.auth.forms import AuthenticationForm

from accounts.models import Profile


class UserForm(AuthenticationForm):
    class Meta:
        model = Profile
        fields = ["username", "password"]
