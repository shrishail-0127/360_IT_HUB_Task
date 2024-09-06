from django.urls import path
from . views import home,register,verify_otp,login


urlpatterns = [
    
    path('home/',home, name='home'),
    path('register/',register, name='register'),
    path('verify-otp',verify_otp,name='verify-otp'),
    path('login/',login,name='login'),
   
]
