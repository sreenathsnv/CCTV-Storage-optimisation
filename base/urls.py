
from django.urls import path,include
from .views import home,login
urlpatterns = [
    path('',home,name = 'home'),
    path('login/',login,name = 'login'),
]