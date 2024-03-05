from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,logout,login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .forms import CustomUserForm
from .models import CustomUser
# Create your views here.


def home(request):

    return render(request,'index.html')

def  loginUser(request):

    return render(request,'Login.html')

def  register(request):
    page = "register"
    if request.method == "POST":
        form = CustomUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            form.save()
            print("user Registered",user.email)


        return redirect('home')            
    context = {'page':page}
    return render(request,'Login.html',context)