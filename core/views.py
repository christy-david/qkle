from django.shortcuts import render

from listing.models import Vehicle,Category,Image
from django.views.decorators.cache import never_cache
from ads.models import Ad

@never_cache
def index(request):
  vehicles = Vehicle.objects.filter(is_sold=False, archived=False,published=True).order_by('-created_at')[:21]

  vehicle_images = {}
  
  for vehicle in vehicles:
    first_image = Image.objects.filter(vehicle_id=vehicle.vehicle_id)[0]
    vehicle_images[vehicle.vehicle_id] = first_image

  categories=Category.objects.all()
  ad=Ad.objects.order_by('?').values('image').first()

  return render(request,'index.html',{
    'vehicles':vehicles,
    'vehicle_images': vehicle_images,
    'categories':categories,
    'ad': ad,
  })
