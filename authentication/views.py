from django.shortcuts import render,redirect
from .forms import SignupForm
from django.views.decorators.cache import never_cache
from django.contrib.auth import logout
from django.contrib.auth import logout, authenticate, login
from authentication.models import CustomUser
from django.contrib import messages
import random
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password
from .forms import LoginForm
from django.core.cache import cache
# from django.contrib.auth import update_session_auth_hash
  
@never_cache
def login_view(request):
    if request.user.is_authenticated:
        return redirect('core:index')
    
    if request.method == 'POST':
        form = LoginForm(request, request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.is_banned:
                    messages.error(request, 'You are banned from the platform.')
                else:
                    login(request, user)
                    messages.success(request, 'You have successfully logged in.')
                    return redirect('core:index')
    else:
        form = LoginForm()

        return render(request, 'authentication/login.html', {'form': form})
    
@never_cache
def logout_user(request):
    logout(request)
    # update_session_auth_hash(request, user)
    cache.clear()
    return redirect(request.META.get('HTTP_REFERER', '/'))

def sign_up(request):
    if request.method=="POST":
        form = SignupForm(request.POST)
        username=request.POST["username"]
        email=request.POST["email"]
        password1=request.POST["password1"]
        password2=request.POST["password2"]
        request.session["username"]=username
        request.session["password"]=password1
        request.session["email"]=email
        if password1==password2:
            if CustomUser.objects.filter(username=username).exists():
                messages.info(request,"Username already exist")
                return redirect('authentication:login')
            elif CustomUser.objects.filter(email=email).exists():
                messages.info(request,"Email already exist")
                return redirect('authentication:login')
            else:
                send_otp(request)
                return render(request,'authentication/otp.html',{"email":email})
        else:
            messages.info(request,"Password mismatch")
            return redirect('authentication:login')
    else:
        form = SignupForm()
        
    return render(request, 'authentication/sign-up.html', {'form': form})

def send_otp(request):
    s=""
    for x in range(0,4):
        s+=str(random.randint(0,9))
    request.session["otp"]=s
    send_mail("otp for sign up",s,'christydavidcruze@gmail.com',[request.session['email']],fail_silently=False)
    return render(request,"authentication/otp.html")

def  otp_verification(request):
    if request.method == 'POST':
        otp_ = request.POST.get("otp")

    if otp_ == request.session["otp"]:
        encrypted_password = make_password(request.session['password'])
        referral_code = request.GET.get('referral_code')
        print("Referral Code:", referral_code)

        if referral_code:
            referred_by_user = CustomUser.objects.filter(referral_code=referral_code).first()
            if referred_by_user:
                # Increase credits for both the new user and the referring user
                nameuser = CustomUser(username=request.session['username'], email=request.session['email'],
                                      password=encrypted_password, referred_by=referred_by_user)
                nameuser.save()

                nameuser.credits += 1
                referred_by_user.credits += 1

                nameuser.save()
                referred_by_user.save()
        else:
            # No referral code provided, save the new user without increasing credits
            nameuser = CustomUser(username=request.session['username'], email=request.session['email'],
                                  password=encrypted_password)
            nameuser.save()

        messages.info(request, 'Account created successfully')
        return redirect('authentication:login')
    else:
        messages.error(request, "Invalid OTP")
        return render(request, 'authentication/otp.html')
    