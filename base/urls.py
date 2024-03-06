
from django.urls import path,include
from .views import home,loginUser,register,userLogout
urlpatterns = [
    path('',home,name = 'home'),
    path('login/',loginUser,name = 'login'),
    path('register/',register,name = 'register'),
    path('logout/',userLogout,name = 'logout'),
    
]