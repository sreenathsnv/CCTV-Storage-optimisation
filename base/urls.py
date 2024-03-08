
from django.urls import path,include
from .views import home,loginUser,register,userLogout,watch,forbidden,adminPanel,viewUser,deleteUser,manageFootage,deleteFootage
urlpatterns = [
    path('',home,name = 'home'),
    
    path('login/',loginUser,name = 'login'),
    path('register/',register,name = 'register'),
    path('logout/',userLogout,name = 'logout'),

    path('watch/',watch,name = 'watch'),
    
    path('forbidden/',forbidden,name = 'forbidden'),

    path('admin-panel/',adminPanel,name = 'adminPanel'),
    path('view-user/',viewUser,name = 'viewUser'),
    path('delete-user/<int:pk>',deleteUser,name = 'deleteUser'),
    path('manage-videos',manageFootage,name = 'manageFootage'),
    path('delete-video/<int:pk>',deleteFootage,name = 'deleteFootage'),


    
]