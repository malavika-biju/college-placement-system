from django.urls import path
from . import views
urlpatterns = [
   path('guest_home/', views.guest_home, name='guest_home'),
   path('login/', views.login, name='login'),
   path('register/', views.register, name='register'),
   path('login_insert/', views.login_insert, name='login_insert'),
   path('companyregistration/', views.register, name='companyregistration'),
   path('get_locations/', views.get_locations_by_district, name='get_locations_by_district'),
   path('login_process/', views.login_process, name='login_process'),
   path('student_register/', views.student_register, name='student_register'),
   path('studentregistration/', views.student_register, name='studentregistration'),
   path('get_batches_by_course/', views.get_batches_by_course, name='get_batches_by_course'),
]

