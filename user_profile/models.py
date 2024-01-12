from django.db import models
import uuid
from listing.models import Vehicle
from django.conf import settings


class Wishlist(models.Model):
  list_id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
  user_id = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='wishlist', on_delete=models.CASCADE)
  vehicle = models.ForeignKey(Vehicle, related_name='wishlist', on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True)

  class Meta:
      ordering = ('-created_at',)

  @classmethod
  def is_vehicle_in_wishlist(cls, user, vehicle):
      return cls.objects.filter(user_id=user, vehicle=vehicle).exists()
