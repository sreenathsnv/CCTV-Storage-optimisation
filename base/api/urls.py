from django.urls import path,include
from .views import loginUser,fileUpload

urlpatterns = [
    path('auth/login/', loginUser, name='api-login'),
    path('upload/', fileUpload, name='api-upload'),
]



