from django.urls import path
from . import views
urlpatterns = [
   path('company_home/', views.company_home, name='company_home'),
   path('jobpost/', views.jobpost, name='jobpost'),
   path('jobpost_insert/', views.jobpost_insert, name='jobpost_insert'),
   path('view_jobpost/', views.view_jobpost, name='view_jobpost'),
   #path('add_job/', views.jobpost, name='add_job'),
   path('edit_job/<int:jobpost_id>/', views.edit_job, name='edit_job'),
   path('delete_job/<int:jobpost_id>/', views.delete_job, name='delete_job'),
   path('index/', views.company_home, name='index'),
   path('requests/', views.company_requests, name='company_requests'),
   path('requests/view/', views.view_requests, name='view_requests'), 
   path('request/view/<int:request_id>/', views.view_request_details, name='view_request_details'),
   path('request/approve/<int:request_id>/', views.approve_request, name='approve_request'),
   path('request/reject/<int:request_id>/', views.reject_request, name='reject_request'),
   path('schedule_job/<int:request_id>/', views.schedule_job, name='schedule_job'),
]
   

