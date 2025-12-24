from django.urls import path
from . import views
urlpatterns = [
   path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
   path('district/', views.district, name='district'),
   path('district_insert/', views.district_insert, name='district_insert'),
    path('district/view/', views.view_districts, name='view_districts'),
   
   
    path('batch/', views.batch, name='batch'),
   path('batch_insert/', views.batch_insert, name='batch_insert'),
   path('delete_district/<int:district_id>/', views.delete_district, name='delete_district'),
  path('edit_district/<int:district_id>/', views.edit_district, name='edit_district'),
   path('view_batch/ ', views.view_batch, name='view_batch'),
   path('delete_batch/<int:batch_id>/', views.delete_batch, name='delete_batch'),
   path('edit_batch/<int:batch_id>/', views.edit_batch, name='edit_batch'),
   path('department/', views.department, name='department'),
   path('department_insert/', views.department_insert, name='department_insert'),
   path('view_department/', views.view_department, name='view_department'),
   path('delete_department/<int:department_id>/', views.delete_department, name='delete_department'),
   path('edit_department/<int:department_id>/', views.edit_department, name='edit_department'),
   path('classtype/', views.classtype, name='classtype'),
   path('classtype_insert/', views.classtype_insert, name='classtype_insert'),
   path('view_classtype/', views.view_classtype, name='view_classtype'),
   path('delete_classtype/<int:classtype_id>/', views.delete_classtype, name='delete_classtype'),
   path('edit_classtype/<int:classtype_id>/', views.edit_classtype, name='edit_classtype'),
   path('location/', views.location, name='location'),
   path('location_insert/', views.location_insert, name='location_insert'),
   path('view_location/', views.view_location, name='view_location'),
   path('delete_location/<int:location_id>/', views.delete_location, name='delete_location'),
   path('edit_location/<int:location_id>/', views.edit_location, name='edit_location'),
   path('filllocation', views.filllocation, name='filllocation'),
   path('course/', views.course, name='course'),
   path('course_insert/', views.course_insert, name='course_insert'),
   path('view_course/', views.view_course, name='view_course'),
   path('fillcourse', views.fillcourse, name='fillcourse'),
   path('delete_course/<int:course_id>/', views.delete_course, name='delete_course'),
   path('edit_course/<int:course_id>/', views.edit_course, name='edit_course'),
   path('trainingclass/', views.trainingclass, name='trainingclass'),
   path('training_class_insert/', views.training_class_insert, name='trainingclass_insert'),
   path('view_trainingclass/', views.view_trainingclass, name='view_trainingclass'),
   path('filltraining', views.filltraining, name='filltraining'),
   path('delete_training/<int:trainingclass_id>/', views.delete_training, name='delete_training'),
   path('edit_training/<int:trainingclass_id>/', views.edit_training, name='edit_training'),




   
  
]