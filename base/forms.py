from django.forms import ModelForm
from .models import CustomUser

class CustomUserForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email','password']