from django import forms
from .models import ChatMessage

class ChatMessageForm(forms.ModelForm):
  class Meta:
    model=ChatMessage
    fields=('message',)
    widgets={
      'message':forms.Textarea(attrs={
        'class': 'w-full py-4 px-6 rounded-xl border'
      })
    }