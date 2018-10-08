from django.contrib.auth.forms import UserCreationForm , forms
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email")


class RatingForm(forms.Form):
    Choice = (('1','1'), ('2', '2'),)
    choices = forms.ChoiceField(widget=forms.Select(), choices=Choice)