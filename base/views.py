from django.shortcuts import render,redirect
from django.contrib.auth import logout,login,authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .forms import CustomUserForm
from .models import CustomUser


# Create your views here.


def userLogout(request):
    logout(request)
    return redirect('home')


def home(request):

    return render(request,'index.html')

def  loginUser(request):

    
    if request.user.is_authenticated:
            return redirect('home')
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = CustomUser.objects.get(email = email)
        except:
            print("error")
        user = authenticate(request,username = email,password = password)
        if user is not None:
            login(request,user)
            
            return redirect('home')
        else:
            print("user is None")


    return render(request,'Login.html')

def  register(request):
    form = CustomUserForm()
    page = "register"
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = CustomUser.objects.create(email = email,username= username)
        user.set_password(password)
        user.save()
        login(request,user)
        return redirect('home')
                    
    context = {'page':page,"form":form}
    print("ruuning")
    return render(request,'Login.html',context)


def listuser(request):
    users = CustomUser.objects.all()
    return render(request,'uploading.html',{"users":users})