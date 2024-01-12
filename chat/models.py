from django.db import models
from listing.models import Vehicle
from django.conf import settings

class Chat(models.Model):
  vehicle=models.ForeignKey(Vehicle,related_name='chats',on_delete=models.CASCADE)
  members=models.ManyToManyField(settings.AUTH_USER_MODEL,related_name='chats')
  created_at=models.DateTimeField(auto_now_add=True)
  modified_at=models.DateTimeField(auto_now=True)

  class Meta:
    ordering=('-modified_at',)

class ChatMessage(models.Model):
  chat=models.ForeignKey(Chat,related_name='messages',on_delete=models.CASCADE)
  message=models.TextField()
  created_at=models.DateTimeField(auto_now_add=True)
  created_by=models.ForeignKey(settings.AUTH_USER_MODEL,related_name='created_messages',on_delete=models.CASCADE)
