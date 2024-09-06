import random
from django.shortcuts import render,redirect
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib.auth import login
from .forms import UserRegisterationForm
from django.contrib import messages
from django.conf import settings
from django.http import HttpResponse

# Create your views here.

def home(request):
    return render(request, 'service/home.html')


def register(request):
    
    if request.method == 'POST':
        form = UserRegisterationForm(request.POST)
        
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            otp = random.randint(100000,999999)
            
            request.session['email'] = email
            request.session['password'] = password
            request.session['otp'] = otp
            
            send_mail('Your OTP for Registeration', f'your OTP is {otp}',settings.EMAIL_HOST_USER,[email],fail_silently=False)
            return redirect('verify-otp')
    
    else:
        form = UserRegisterationForm()
        
    return render(request, 'service/register.html', {'form':form})
    
        
        
def verify_otp(request):
    
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        
        generated_otp = request.session.get('otp')
        email  = request.session.get('email')
        password = request.session.get('password')
        
        if not generated_otp or not email or not password:
            messages.error(request, 'Session expired or invalid. Please register again.')
            return redirect('register')
        
        if entered_otp and int(entered_otp) == generated_otp:
            
            if User.objects.filter(username=email).exists():
                messages.error(request, 'A user with this email already exists. Please log in.')
                return redirect('login')
            
            user = User.objects.create_user(username=email, password = password)
            user.save()
            login(request,user)
            
            del request.session['otp']
            del request.session['email']
            del request.session['password']
            
            messages.success(request, "Registeration Successful please login!")
            return redirect('login')
        
        else:
            messages.error(request,"Invalid OTP please try again!")
            return redirect('verify-otp')
    
    
    
    return render(request, 'service/verify_otp.html')

def login_user(request):
    return redirect(request, 'service/login.html')