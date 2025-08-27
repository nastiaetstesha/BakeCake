from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Customer


class SignUpForm(UserCreationForm):
    email = forms.EmailField(label='Email', required=False)
    phone = forms.CharField(label='Телефон', max_length=32, required=False)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email',)

    def save(self, commit=True):
        user = super().save(commit=commit)
        # создаём профиль покупателя
        phone = self.cleaned_data.get('phone', '')
        if commit:
            Customer.objects.create(user=user, phone=phone)
        else:
            user._deferred_customer_phone = phone
        return user
