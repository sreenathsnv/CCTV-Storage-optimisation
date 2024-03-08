from django.shortcuts import render,redirect
from django.contrib.auth import logout,login,authenticate
from django.contrib.auth.decorators import login_required
from .forms import CustomUserForm
from .models import CustomUser,Footages
from django.contrib import messages



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
        except CustomUser.DoesNotExist:
            
            messages.error(request, 'No user available.Register')
            return render(request,'Login.html')
            

        user = authenticate(request,username = email,password = password)
        if user is not None:
            login(request,user)
            # if user.is_staff:
            #     return render(request,'admin.html')
                
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')
            return render(request,'Login.html')
            
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
    return render(request,'Login.html',context)


@login_required(login_url='login')
def watch(request):

    footages = Footages.objects.filter(user = request.user)
    context = {"footages":footages}
    return render(request,'footages.html',context)


def forbidden(request):
        return render(request,'forbidden.html')



@login_required(login_url='login')
def adminPanel(request):
    if not request.user.is_staff:
        return redirect('forbidden')
    
    return render(request,'admin.html')

def viewUser(request):
    users = CustomUser.objects.all()

    if not request.user.is_staff:
        return redirect('forbidden')
    context = {"users":users}
    return render(request,'users.html',context)        

@login_required(login_url='login')
def manageFootage(request):
    if not request.user.is_staff:
        return redirect('forbidden')
    users = CustomUser.objects.all()
    footages = None
    if request.method == "GET":
        user_id = request.GET.get('user')
        print(user_id)
        if user_id:
            footages = Footages.objects.filter(user_id=user_id)
    context = {"users":users,"footages":footages}
    return render(request,'footages.html',context)


@login_required(login_url='login')
def deleteFootage(request,pk):
    footage = Footages.objects.get(id = pk)
    if not request.user.is_staff:
        return redirect('forbidden')
    if request.method == "POST":
        footage.delete()
        return redirect('manageFootage')
    return render(request,'delete.html')


@login_required(login_url='login')
def deleteUser(request,pk):
    if not request.user.is_staff:
        return redirect('forbidden')
    
    user = CustomUser.objects.get(id = pk)
    context = {"user":user}

    if request.method == "POST":
        user.delete()
        return redirect('viewUser')

    return render(request,'delete.html',context)