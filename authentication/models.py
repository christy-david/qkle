from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
import random
import string
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
  id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
  credits = models.IntegerField(default=1)
  is_banned = models.BooleanField(default=False)
  referral_code = models.CharField(max_length=8, unique=True, null=True, blank=True)

  groups = models.ManyToManyField(
      "auth.Group",
      related_name="custom_user_set",
      related_query_name="custom_user",
      blank=True,
      verbose_name="groups",
      help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
  )
  user_permissions = models.ManyToManyField(
      "auth.Permission",
      related_name="custom_user_set",
      related_query_name="custom_user",
      blank=True,
      verbose_name="user permissions",
      help_text="Specific permissions for this user.",
  )

  def save(self, *args, **kwargs):
      # Generate a unique referral code if not provided
      if not self.referral_code:
          self.referral_code = self.generate_unique_referral_code()
      super().save(*args, **kwargs)

  def generate_unique_referral_code(self):
      # Generate a random 8-character referral code
      while True:
          referral_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
          if not CustomUser.objects.filter(referral_code=referral_code).exists():
              return referral_code