
from django.urls import path,include
from .views import home,loginUser,register
urlpatterns = [
    path('',home,name = 'home'),
    path('login/',loginUser,name = 'login'),
    path('register/',register,name = 'register'),
]