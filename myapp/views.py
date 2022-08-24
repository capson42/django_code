import email
from django.shortcuts import render,redirect          #this renders the html file from the views 
from django.http import HttpResponse             #this is to use http response to get request and post request
from .models import Feature                      #this is to import features model from the models module  
from django.contrib.auth.models import User #this is basically used to authenticate user in db
from django.contrib import messages              #this basically is used to store temporary flashes messages to guide
                                                 #the user.
from django.contrib.auth import authenticate
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import login as auth_login

# Create your views here.

#The purpose of this index view is to get the all the records from the feature table.
#and then send the info to the html for rendering.

def index(request):
    features=Feature.objects.all()
    return render(request,'index.html',{'features':features})

#The purpose of this code to read the amount of words entered in the text area 

def counter(request):
    text=request.POST['words']
    amount_of_words=len(text.split())
    return render(request,'counter.html',{'amount':amount_of_words})

#The purpose of this register view is to take in the data that is posted from the register form and use it.
#it also checks if the email already exists in the db, if confirm password and password matches, if the request
#that is made by the user is post.


def register(request):
    if request.method=='POST':
        email=request.POST['email']
        username=request.POST['username']
        password=request.POST['password']
        confirm_password=request.POST['confirmpassword']

        if password==confirm_password:
            if User.objects.filter(email=email).exists():
                messages.info(request,"email already exists")
                return redirect('register')
            elif User.objects.filter(username=username).exists():
                messages.info(request,'Username already exists')
                return redirect('register')
            else:
                messages.info(request,'Username created successfully')
                user=User.objects.create_user(username=username,email=email,password=password)
                user.save()
                return redirect('login')
        else:
            messages.info(request,"passwords doesn't match with confirm password")
            return redirect('register')

    else:
        return render(request,'register.html')

def login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(request,username=username,password=password)
        if user is not None:
            auth_login(request,user)
            return redirect('/')
        else:
            messages.info(request,'Invalid Credentials')
            return redirect('login')
    else:
        return render(request,'login.html')

def logout(request):
    auth_logout(request)
    return redirect('/')

def post(request,pk):
    return render(request,'post.html',{'pk':pk})
