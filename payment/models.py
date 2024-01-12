from django.db import models
import uuid
from django.conf import settings

class Transaction(models.Model):
  payment_id=models.UUIDField(default=uuid.uuid4,primary_key=True,editable=False)
  razorpay_payment_id=models.CharField(max_length=255)
  razorpay_order_id=models.CharField(max_length=255)
  buyer_id=models.ForeignKey(settings.AUTH_USER_MODEL,related_name='users',on_delete=models.CASCADE)
  amount=models.FloatField(default=169.00)
  credits=models.IntegerField(default=1)
  coupon = models.ForeignKey('Coupon', on_delete=models.SET_NULL, null=True, blank=True)
  timestamp=models.DateTimeField(auto_now_add=True)

class Coupon(models.Model):
  coupon_id=models.UUIDField(default=uuid.uuid4,primary_key=True,editable=False)
  coupon_code=models.CharField(max_length=255)
  discount_value=models.IntegerField()
  TYPES = [
    ('percentage', 'Percentage discount'),
    ('flat', 'Flat discount'),
  ]
  discount_type=models.CharField(max_length=100,choices=TYPES)
  expiry_date=models.DateField()