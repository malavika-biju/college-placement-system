from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
#from .models import tbl_district, tbl_batch, tbl_department, tbl_classtype, tbl_location, tbl_course, tbl_trainingclass

def company_home(request):
    return render(request, 'company/index.html')
def myjobs(request):
    return render(request, 'company/myjobs.html')
