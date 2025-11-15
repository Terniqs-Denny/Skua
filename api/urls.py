# api/urls.py
from django.urls import path, include

urlpatterns = [
    path('', include('api.users.urls')),  
    
    
    path('users/', include('api.users.urls')),
    path('auth/', include('api.userauth.urls')),
]