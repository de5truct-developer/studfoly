from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'placeholder': 'your@email.com'})
    )
    first_name = forms.CharField(
        label='Имя', max_length=30,
        widget=forms.TextInput(attrs={'placeholder': 'Ваше имя'})
    )
    last_name = forms.CharField(
        label='Фамилия', max_length=30,
        widget=forms.TextInput(attrs={'placeholder': 'Ваша фамилия'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Имя пользователя'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs['placeholder'] = 'Пароль'
        self.fields['password2'].widget.attrs['placeholder'] = 'Подтвердите пароль'
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Фамилия'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
        }


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            'avatar', 'bio', 'title', 'city', 'phone', 'telegram',
            'github', 'linkedin', 'website', 'skills_summary', 'is_available'
        ]
        widgets = {
            'avatar': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'bio': forms.Textarea(attrs={
                'class': 'form-control', 'rows': 4,
                'placeholder': 'Расскажите о себе...'
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Например: Frontend Developer'
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Ваш город'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': '+7 (999) 123-45-67'
            }),
            'telegram': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': '@username'
            }),
            'github': forms.URLInput(attrs={
                'class': 'form-control', 'placeholder': 'https://github.com/username'
            }),
            'linkedin': forms.URLInput(attrs={
                'class': 'form-control', 'placeholder': 'https://linkedin.com/in/username'
            }),
            'website': forms.URLInput(attrs={
                'class': 'form-control', 'placeholder': 'https://example.com'
            }),
            'skills_summary': forms.Textarea(attrs={
                'class': 'form-control', 'rows': 3,
                'placeholder': 'Кратко опишите ваши ключевые навыки...'
            }),
            'is_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
