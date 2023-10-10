from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import Customers


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = Customers
        fields = ("email","first_name","last_name")


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = Customers
        fields = ("email","first_name","last_name")
