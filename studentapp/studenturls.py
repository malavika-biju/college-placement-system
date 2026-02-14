from django.urls import path
from . import views
urlpatterns = [
    path('student_home/', views.student_home, name='student_home'),
    path("student_trainingclass/", views.student_trainingclass, name="student_trainingclass"),
    path("student_accepted_jobs/", views.student_accepted_jobs, name="student_accepted_jobs"),
    path("myprofile/", views.myprofile, name="myprofile"),
    path("resume/", views.resume, name="resume"),
    path("logout/", views.logout_view, name="logout"),
    path("update_profile/", views.update_profile, name="update_profile"),
    
]