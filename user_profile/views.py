from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from listing.models import Vehicle,Image
from .models import Wishlist
from django.views.decorators.cache import never_cache
import random
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from authentication.models import CustomUser
from .forms import UserEditForm
from django.contrib.auth.forms import PasswordChangeForm
from django.core.cache import cache

@login_required
@never_cache
def user_listings(request):
  vehicles=Vehicle.objects.filter(sold_by=request.user,archived=False)

  return render(request,'user_profile/listings.html',{
    "vehicles": vehicles
  })

@login_required
@never_cache
def wishlist(request):
  wishlist = Wishlist.objects.filter(user_id=request.user)
  vehicles = {}
  vehicle_images = {}

  for item in wishlist:
      vehicle = Vehicle.objects.filter(vehicle_id=item.vehicle_id).first()
      vehicles[item.vehicle_id] = vehicle

      # Get the first image for each vehicle
      first_image = Image.objects.filter(vehicle_id=item.vehicle_id).first()
      vehicle_images[item.vehicle_id] = first_image

  return render(request, 'user_profile/wishlist.html', {
      "wishlist": wishlist,
      'vehicles': vehicles,
      'vehicle_images': vehicle_images,
  })

def reset_password(request):
  if request.method=="POST":
        email=request.POST["email"]
        request.session["email"]=email
        send_otp(request)

        return render(request,'user_profile/otp.html',{"email":email})
        
        
  return render(request, 'user_profile/reset_password.html', {
       
  })
    
def send_otp(request):
    s=""
    for x in range(0,4):
        s+=str(random.randint(0,9))
    request.session["otp"]=s
    send_mail("otp for sign up",s,'christydavidcruze@gmail.com',[request.session['email']],fail_silently=False)
    return render(request,"user_profile/otp.html")

def  otp_verification(request):
    if  request.method=='POST':
        otp_=request.POST.get("otp")
        password=request.POST.get("password")
        confirm_password=request.POST.get("confirm_password")
    if otp_ == request.session["otp"] and password==confirm_password and password!='':
        email=request.session['email']
        encryptedpassword=make_password(password)
        to_update = CustomUser.objects.get(email=email)
        to_update.password=encryptedpassword
        to_update.save()
        messages.info(request,'Password reset successful')
        return redirect('authentication:login')
    else:
        if otp_!=request.session["otp"]:
          messages.error(request,"Invalid OTP")
          return render(request,'user_profile/otp.html')
        if password!=confirm_password:
            messages.error(request,"New passwords does not match")
            return render(request,'user_profile/otp.html')
        if password=='':
            messages.error(request,"Password cannot be empty")
            return render(request,'user_profile/otp.html')

@login_required
def edit_profile(request):
  if request.method == 'POST':
    form = UserEditForm(request.POST, instance=request.user)
    if form.is_valid():
      form.save()
      messages.success(request, 'Profile updated successfully.')
      return redirect('user_profile:edit-profile')
  else:
    form = UserEditForm(instance=request.user)

  return render(request, 'user_profile/edit_profile.html', {'form': form})

def view_profile(request, user_id):
    user = CustomUser.objects.get(id=user_id)
    return render(request, 'user_profile/view_profile.html', {'user': user})


@login_required
def reset_password_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            cache.clear()  # Clear the cache
            messages.success(request, 'Your password was successfully updated!')
            return redirect('core:index')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'user_profile/forgot_password.html', {'form': form})