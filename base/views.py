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


    if request.user.is_authenticated():
            return redirect('home')
    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        try:
            user = CustomUser.objects.get(email = email)
        except:
            print("error")
        user = authenticate(user,email = email,password = password)
        if user is not None:
            login(request,user)
            context = {"username":user.username}
            return redirect('home',context)


    return render(request,'Login.html')

def  register(request):
    page = "register"
    if request.method == "POST":
        form = CustomUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            form.save()
            context = {"username":user.username}
        return redirect('home',context)            
    context = {'page':page}
    return render(request,'Login.html',context)