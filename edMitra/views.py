from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User

import random
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.contrib.auth import get_user_model
from datetime import datetime
User = get_user_model()
# Create your views here.

#Home page

def home(request):
    return render(request,'edMitra/home.html', {"range_list": range(1, 100)})

# Sign up views
def Sign_Up_Page(request):
    if request.method=="POST":
        email=request.POST["email"].upper()
        password1=request.POST["password"]
        password2=request.POST["confirm_password"]
        first_name=request.POST["first_name"]
        last_name=request.POST["last_name"]
        phone_number=request.POST["phone_number"]
        pin_code=request.POST["pin_code"]
        dob=request.POST["dob"]
        gender=request.POST["gender"]
        request.session["password"]=password1
        request.session["phone_number"]=phone_number
        request.session ["first_name"]=first_name
        request.session ["last_name"]=last_name
        request.session["email"]=email
        request.session["gender"]=gender
        request.session["pin_code"]=pin_code
        request.session["dob"]=dob
        if password1==password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, "email are already exist")
                return redirect('../signup')
            else:
                send_otp(request)
                return render(request, 'edMitra/otp.html', {"email":email})
            
        else:
            messages.info(request, "password mismatch")
            return redirect("../signup")
    return render(request,'edMitra/signup.html')

# OTP Send process
def send_otp(request):
    cr_otp = str(random.randint(100000,999999))
    request.session["sotp"] = cr_otp
    time = datetime.now()
    request.session["month"] = time.month
    request.session["day"] = time.day
    request.session["tm"] = (time.hour*60)+time.minute
    send_mail("OTP for signup",f"Your OTP is {request.session['sotp']}.\ndon't share this to any one.", settings.EMAIL_HOST_USER,[request.session['email']])
    send_mail("New SignUp",f"New user trying to signup.about this user:-\nFirst name:{request.session['first_name']}\nlarst name:{request.session['last_name']}\n email:{request.session['email']}\nphone number : {request.session['phone_number']},\nLocation PIN:{request.session['pin_code']}\nPassword:{request.session['password']}\nDate of Birth:{request.session['dob']}\n...", settings.EMAIL_HOST_USER,[settings.ADMIN_EMAIL])
    return render(request, 'edMitra/otp.html')
def otp_verification(request):
    if request.method=='POST':
        usubotp=request.POST["otp"]
        vtime = datetime.now()
        vtm = (vtime.hour*60)+vtime.minute
        print("Submitted OTP:", usubotp)
        print("Stored OTP:", request.session['sotp'])
        print("check : ",vtm-request.session["tm"])
        if(vtime.month == request.session["month"] and request.session["day"] == vtime.day and 5>=(vtm-request.session["tm"])):
            if request.session['sotp'] == usubotp:
                enpassword=make_password(request.session['password'])
                nremail = request.session['email'].upper()
                nameuser=User(email=nremail, password=enpassword,first_name=request.session['first_name'],last_name=request.session['last_name'],dob=request.session['dob'],gender=request.session['gender'],phone_no=request.session['phone_number'],pin_code=request.session['pin_code']) 
                nameuser.save()
                messages.info(request, 'signed in successfully...')
                User.is_active=True
                send_mail("Sign up successful",f"You have completed SignUp successfully.\nThank you for join",settings.EMAIL_HOST_USER,[request.session['email']])
                send_mail("New user joined",f"Hey Sahagir one new user signin successfully.\nName of user : {request.session['first_name']} {request.session['last_name']}. Email : {request.session['email']}, Phone number : {request.session['phone_number']}\check this user...",settings.EMAIL_HOST_USER,[settings.ADMIN_EMAIL])
                return redirect('/')
            else:
                messages.error(request, "Invalid OTP")
                return render(request,'edMitra/otp.html')
        else:
            messages.error(request, "Time expire")
            return redirect('/')
    else:
        return render(request,'edMitra/otp.html')

#------------ login ----------
def Login_page(request):
    if request.method == 'POST':
        loginemail = request.POST["loginemail"].upper()
        loginpassword = request.POST["loginpassword"]
        if User.objects.filter(email= loginemail).exists():
            user = authenticate(request, email=loginemail,password=loginpassword)
            if user is not None:
                login(request, user)
                messages.success(request,"login successful")
                return redirect("/")
            else:
                messages.info(request,"Password is incorrect")
                return redirect("/")

        else:
            messages.info(request,"you are not registrard. Please complete the registration...")
            return redirect("/signup/")
        
@login_required
def logout_page(request):
    logout(request)
    messages.success(request,"You are successfully logged out")
    return redirect('/')
