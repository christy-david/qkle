from django.db import models
import uuid
from django.conf import settings

class Category(models.Model):
  category_id=models.UUIDField(default=uuid.uuid4,primary_key=True,editable=False)
  name=models.CharField(max_length=255)
  created_at=models.DateTimeField(auto_now_add=True)
  archived=models.BooleanField(default=False)

  class Meta:
    ordering=('name',)
    verbose_name_plural="Categories"

  def __str__(self):
    return self.name
  

class VehicleMake(models.Model):
  make_id=models.UUIDField(default=uuid.uuid4,primary_key=True,editable=False)
  name=models.CharField(max_length=255)
  created_at=models.DateTimeField(auto_now_add=True)

  class Meta:
    ordering=('name',)
    verbose_name_plural="Makers"

  def __str__(self):
    return self.name


class VehicleModel(models.Model):
  model_id=models.UUIDField(default=uuid.uuid4,primary_key=True,editable=False)
  make=models.ForeignKey(VehicleMake,related_name='models',on_delete=models.CASCADE)
  name=models.CharField(max_length=255)

  class Meta:
    ordering=('name',)
    verbose_name_plural="Models"

  def __str__(self):
    return self.name


class Vehicle(models.Model):
  vehicle_id=models.UUIDField(default=uuid.uuid4,primary_key=True,editable=False)
  make=models.ForeignKey(VehicleMake,related_name='items',on_delete=models.CASCADE)
  model=models.ForeignKey(VehicleModel,related_name='items',on_delete=models.CASCADE)
  price=models.FloatField()
  category=models.ForeignKey(Category,related_name='items',on_delete=models.CASCADE)
  kms_driven=models.IntegerField()
  FUEL_TYPES=[
    ('petrol','Petrol'),
    ('diesel','Diesel'),
    ('cng','CNG'),
    ('electric','Electric'),
    ('lpg','LPG'),
    ('hybrid','Hybrid'),
  ]
  fuel_type=models.CharField(max_length=100,choices=FUEL_TYPES,default=None)
  TRANSMISSIONS=[
    ('manual','Manual'),
    ('automatic','Automatic'),  
  ]
  transmission=models.CharField(max_length=100,choices=TRANSMISSIONS,default=None)
  OWNERS=[
    ('1','1st owner'),
    ('2','2nd owner'),
    ('3','3rd owner'),
    ('4','4th owner'),
    ('4+','More than 4 owners'),
  ]
  no_of_owners=models.CharField(max_length=100,choices=OWNERS,default=None)
  location=models.CharField(max_length=255)
  registered_year=models.IntegerField()
  additional_details=models.TextField()
  sold_by=models.ForeignKey(settings.AUTH_USER_MODEL,related_name='items',on_delete=models.CASCADE)
  created_at=models.DateTimeField(auto_now_add=True)
  is_sold=models.BooleanField(default=False)
  featured=models.BooleanField(default=False)
  archived=models.BooleanField(default=False)
  published=models.BooleanField(default=False)

  class Meta:
    ordering=('created_at',)
    verbose_name_plural="Vehicles"

  def __str__(self):
    return f"{self.registered_year} {self.make} {self.model}."
  
class Image(models.Model):
  image_id=models.UUIDField(default=uuid.uuid4,primary_key=True,editable=False)
  vehicle_id=models.ForeignKey(Vehicle,related_name='images',on_delete=models.CASCADE)
  created_at=models.DateTimeField(auto_now_add=True)

  def vehicle_image_upload_to(instance, filename):
    directory_name=instance.vehicle_id.vehicle_id
    file_extension = filename.split('.')[-1]
    file_name=f'{instance.vehicle_id.images.count() + 1 }.{file_extension}'
    return f'vehicle-images/{directory_name}/{file_name}'
  
  image=models.ImageField(upload_to=vehicle_image_upload_to)

  def __str__(self):
    return f"Image for {self.vehicle_id.registered_year} {self.vehicle_id.make} {self.vehicle_id.model}"