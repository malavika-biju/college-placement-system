from django.urls import path
from . import views
urlpatterns = [
   path('company_home/', views.company_home, name='company_home'),
   path('myjobs/', views.myjobs, name='myjobs'),

]