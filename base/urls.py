
from django.urls import path,include
from .views import home,loginUser,register,userLogout,watch,forbidden,adminPanel
urlpatterns = [
    path('',home,name = 'home'),
    
    path('login/',loginUser,name = 'login'),
    path('register/',register,name = 'register'),
    path('logout/',userLogout,name = 'logout'),

    path('watch/',watch,name = 'watch'),
    
    path('forbidden/',forbidden,name = 'forbidden'),

    path('admin-panel/',adminPanel,name = 'adminPanel'),

    
]