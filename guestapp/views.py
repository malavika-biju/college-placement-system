from datetime import date
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import tbl_login, tbl_company
from adminapp.models import tbl_location 


def guest_home(request):
    return render(request, 'guest/index.html')
def login(request):
    return render(request, 'guest/login.html')
def register(request):
    
    return render(request, 'guest/register.html', {'locations': tbl_location.objects.all()})


def login_insert(request):
    if request.method == "POST":
        # Create login object
        lob = tbl_login()
        lob.username = request.POST.get("username")
        lob.password = request.POST.get("password")
        lob.role = "company"  # Changed from "member" to "company"
        lob.status = "requested"
        
        # Check if username already exists
        if tbl_login.objects.filter(username=request.POST.get("username")).exists():
            return HttpResponse("<script>alert('Username Already Exists..');window.location='/companyregistration';</script>")
        else:
            # Get form data for company
            company_name = request.POST.get("company_name")
            location_id = request.POST.get("location_id")
            company_logo = request.FILES.get("company_logo")
            contact_number = request.POST.get("contact_number")
            contact_email = request.POST.get("contact_email")
            id_proof = request.FILES.get("id_proof")
            
            # Check if company already exists in this location
            if tbl_company.objects.filter(company_name=company_name, location_id=location_id).exists():
                return HttpResponse("<script>alert('Company already exists in this location');window.location='/companyregistration';</script>") 
            else:
                # Get location object
                try:
                    location_obj = tbl_location.objects.get(location_id=location_id)
                except tbl_location.DoesNotExist:
                    return HttpResponse("<script>alert('Invalid Location');window.location='/companyregistration';</script>")
                
                # Save login first
                lob.save()
                
                # Create company object
                com = tbl_company()
                com.company_name = company_name
                com.location_id = location_obj
                com.company_logo = company_logo
                com.contact_number = contact_number
                com.contact_email = contact_email
                com.id_proof = id_proof
                com.login_id = lob
                com.reg_date = date.today()
                com.save()

                return HttpResponse("<script>alert('Successfully Registered');window.location='/companyregistration';</script>")