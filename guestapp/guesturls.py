from django.urls import path
from . import views
urlpatterns = [
   path('guest_home/', views.guest_home, name='guest_home'),
   path('login/', views.login, name='login'),
   path('register/', views.register, name='register'),
   path('login_insert/', views.login_insert, name='login_insert'),
   
]

