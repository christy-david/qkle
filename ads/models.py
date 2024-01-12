from django.db import models
import uuid

class Ad(models.Model):
  campaign_id=models.UUIDField(default=uuid.uuid4,primary_key=True,editable=False)
  image=models.ImageField(upload_to='ad-campaigns/ads')
  created_at=models.DateTimeField(auto_now_add=True)