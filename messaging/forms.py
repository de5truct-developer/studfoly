from django import forms
from .models import Message


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control message-input',
                'rows': 1,
                'placeholder': 'Напишите сообщение...',
            }),
        }
        labels = {
            'text': '',
        }
