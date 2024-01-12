from django.shortcuts import render, get_object_or_404,redirect
from .models import Vehicle,Category,Image
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from .forms import NewItemForm, EditItemForm, ImageForm
from django.db.models import Q
from django.contrib import messages
from ads.models import Ad
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from user_profile.models import Wishlist

@never_cache
def details(request,pk):
  vehicle = get_object_or_404(Vehicle, pk=pk)
  vehicle_images = Image.objects.filter(vehicle_id=pk).values('image_id', 'vehicle_id', 'image')
  # vehicle_images = Image.objects.filter(vehicle_id=pk)
  related = Vehicle.objects.filter(category=vehicle.category, is_sold=False).exclude(pk=pk).order_by('?')[0:4]
  related_vehicle_images = {}
  
  for v in related:
    first_image = Image.objects.filter(vehicle_id=v.vehicle_id)[0]
    related_vehicle_images[v.vehicle_id] = first_image

  ad=Ad.objects.order_by('?').values('image').first()

  return render(request, 'listing/details.html', {
    'vehicle': vehicle,
    'vehicle_images': list(vehicle_images),
    # 'vehicle_images': vehicle_images,
    'related': related,
    'related_vehicle_images': related_vehicle_images,
    'ad': ad,
  })

@never_cache
def search_listing(request):
    query = request.GET.get('query', '')
    category_id = request.GET.get('category', '')
    sort_by = request.GET.get('sort_by', '-created_at')  # Default sorting by created_at

    vehicles = Vehicle.objects.filter(is_sold=False, archived=False)
    vehicle_count=vehicles.count()
    vehicle_images = {}

    for vehicle in vehicles:
        first_image = Image.objects.filter(vehicle_id=vehicle.vehicle_id).first()
        vehicle_images[vehicle.vehicle_id] = first_image

    categories = Category.objects.all()

    if category_id:
        vehicles = vehicles.filter(category_id=category_id)

    if query:
        vehicles = vehicles.filter(Q(make__name__icontains=query) | Q(model__name__icontains=query))

    vehicles = vehicles.order_by(sort_by)

    # Pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(vehicles, 1)  # Change later to show 50 vehicles per page

    try:
        vehicles = paginator.page(page)
    except PageNotAnInteger:
        vehicles = paginator.page(1)
    except EmptyPage:
        vehicles = paginator.page(paginator.num_pages)

    return render(request, 'listing/search.html', {
        'vehicles': vehicles,
        'vehicle_count': vehicle_count,
        'vehicle_images': vehicle_images,
        'query': query,
        'categories': categories,
        'category_id': category_id,
        'sort_by': sort_by,
    })

@never_cache
@login_required
def sell(request):
  if request.user.credits<=0:
    return render(request, 'payment/no_credits.html')
  
  if request.user.is_banned:
    return render(request, 'payment/user_banned.html')
  
  elif request.method == 'POST':
    form = NewItemForm(request.POST)
    images=request.FILES.getlist('image')

    if form.is_valid():
      vehicle = form.save(commit=False)
      vehicle.sold_by = request.user
      vehicle.save()

      for i in images:
        Image.objects.create(vehicle_id=vehicle,image=i)
      
      request.user.credits-=1
      request.user.save()
      
      messages.success(request,'New vehicle added')
        
      return redirect('listing:details', pk=vehicle.vehicle_id)
    else:
      print(form.errors)
  else:
    form = NewItemForm()
    image_form=ImageForm()

  return render(request, 'listing/sell.html', {
    'form': form,
    'image_form': image_form,
  })

@never_cache
@login_required
def edit(request,pk):
  vehicle=get_object_or_404(Vehicle,pk=pk,sold_by=request.user)
  if request.method == 'POST':
    form = EditItemForm(request.POST, request.FILES,instance=vehicle)

    if form.is_valid():
      vehicle.save()

      return redirect('listing:details', pk=vehicle.vehicle_id)
  else:
    form = EditItemForm(instance=vehicle)

  return render(request, 'listing/sell.html', {
    'form': form,
  })

@never_cache
@login_required
def archive_listing(request,pk):
  vehicle=get_object_or_404(Vehicle,pk=pk,sold_by=request.user)
  vehicle.archived=True
  vehicle.save()

  return redirect('user_profile:user-listings')

@login_required
def toggle_wishlist(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, vehicle_id=vehicle_id)
    user = request.user

    is_in_wishlist = Wishlist.is_vehicle_in_wishlist(user, vehicle)

    if is_in_wishlist:
        Wishlist.objects.filter(user_id=user, vehicle=vehicle).delete()
    else:
        Wishlist.objects.create(user_id=user, vehicle=vehicle)

    return JsonResponse({'is_in_wishlist': not is_in_wishlist})
