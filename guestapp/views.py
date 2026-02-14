from datetime import date
from django.core.mail import send_mail
from urllib import request 
from django.shortcuts import redirect
from django.shortcuts import render, redirect 
from django.http import HttpResponse, JsonResponse
from .models import tbl_login, tbl_company, tbl_student
from adminapp.models import tbl_location, tbl_district, tbl_course, tbl_batch


def guest_home(request):
    return render(request, 'guest/index.html')

def login(request):
    return render(request, 'guest/login.html')


def logoutfun(request):
    request.session.clear()
    return redirect('/guestapp/guest_home/')

def login_insert(request):
    if request.method == "POST":
        role = request.POST.get("role", "company")
        
        if role == "student":
            lob = tbl_login()
            lob.username = request.POST.get("username")
            lob.password = request.POST.get("password")
            lob.role = "student" 
            lob.status = "requested"
            
            if tbl_login.objects.filter(username=request.POST.get("username")).exists():
                return HttpResponse("<script>alert('Username Already Exists..');window.location='/guestapp/studentregistration/';</script>")
            else:
                student_name = request.POST.get("student_name")
                course_id = request.POST.get("course_id")
                batch_id = request.POST.get("batch_id")
                email = request.POST.get("email")
                contact_number = request.POST.get("contact_number")
                gender = request.POST.get("gender")
                mark = request.POST.get("mark", 0)
                percentage = request.POST.get("percentage", 0)
                
                resume = request.FILES.get("resume")
                id_proof = request.FILES.get("id_proof")
                photo = request.FILES.get("photo")
                
                try:
                    course_obj = tbl_course.objects.get(course_id=course_id)
                    batch_obj = tbl_batch.objects.get(batch_id=batch_id)
                except (tbl_course.DoesNotExist, tbl_batch.DoesNotExist):
                    return HttpResponse("<script>alert('Invalid Course or Batch');window.location='/guestapp/studentregistration/';</script>")
                
                if tbl_student.objects.filter(email=email).exists():
                    return HttpResponse("<script>alert('Email Already Exists');window.location='/guestapp/studentregistration/';</script>")
                
                lob.save()
                
                student = tbl_student()
                student.student_name = student_name
                student.course_id = course_obj
                student.batch_id = batch_obj
                student.email = email
                student.contact_number = contact_number
                student.gender = gender
                student.mark = float(mark) if mark else 0.0
                student.percentage = float(percentage) if percentage else 0.0
                student.resume = resume
                student.id_proof = id_proof
                student.photo = photo
                student.login_id = lob
                student.save()

                send_mail(
                    'Registration Completed',
                    'Your student registration has been completed successfully.',
                    'malumr2006@gmail.com',
                    [email]
                )

                return HttpResponse("<script>alert('Successfully Registered as Student');window.location='/guestapp/studentregistration/';</script>")
        
        else:
            lob = tbl_login()
            lob.username = request.POST.get("username")
            lob.password = request.POST.get("password")
            lob.role = "company" 
            lob.status = "requested"
            
            if tbl_login.objects.filter(username=request.POST.get("username")).exists():
                return HttpResponse("<script>alert('Username Already Exists..');window.location='/guestapp/companyregistration/';</script>")
            else:
                company_name = request.POST.get("company_name")
                location_id = request.POST.get("location_id")
                company_logo = request.FILES.get("company_logo")
                contact_number = request.POST.get("contact_number")
                contact_email = request.POST.get("contact_email")
                id_proof = request.FILES.get("id_proof")
                
                if tbl_company.objects.filter(company_name=company_name, location_id=location_id).exists():
                    return HttpResponse("<script>alert('Company already exists in this location');window.location='/guestapp/companyregistration/';</script>") 
                else:
                    try:
                        location_obj = tbl_location.objects.get(location_id=location_id)
                    except tbl_location.DoesNotExist:
                        return HttpResponse("<script>alert('Invalid Location');window.location='/guestapp/companyregistration/';</script>")
                    
                    lob.save()
                    
                    
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

                    send_mail(
                        'Registration Completed',
                        'Your company registration has been completed successfully.',
                        'malumr2006@gmail.com',
                        [contact_email]
                    )

                    return HttpResponse("<script>alert('Successfully Registered');window.location='/guestapp/companyregistration/';</script>")
    else:
        return HttpResponse("<script>alert('Invalid Request Method');window.location='/guestapp/companyregistration/';</script>")
    


def register(request):
    districts = tbl_district.objects.all()
    return render(request, 'guest/register.html', {'districts': districts})

def student_register(request):
    courses = tbl_course.objects.all()
    batches = tbl_batch.objects.all()
    return render(request, 'guest/student_register.html', {
        'courses': courses,
        'batches': batches
    })

def company_registration(request):
    districts = tbl_district.objects.all()
    return render(request, 'guest/register.html', {'districts': districts})

def student_registration(request):
    courses = tbl_course.objects.all()
    batches = tbl_batch.objects.all()
    return render(request, 'guest/student_register.html', {
        'courses': courses,
        'batches': batches
    })

def get_locations_by_district(request):
    if request.method == 'GET':
        district_id = request.GET.get('district_id')
        
        if district_id:
            locations = tbl_location.objects.filter(district_id=district_id).values('location_id', 'location_name')
            locations_list = list(locations)
            
            return JsonResponse({
                'success': True,
                'locations': locations_list
            })
    
    return JsonResponse({'success': False, 'locations': []})


def login_process(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        if tbl_login.objects.filter(username=username, password=password).exists():
            logindata = tbl_login.objects.get(username=username, password=password)
            request.session['login_id'] = logindata.login_id
            role = logindata.role
            status = logindata.status
            if role == "admin":
                return redirect('/adminapp/dashboard')
            elif role == "company":
                if status == "confirmed":
                    return redirect('/companyapp/company_home')
                else:
                    return render(request, "guest/login.html", {"error": "Your account is pending approval. Please contact admin."})
            elif role == "student":
                if status == "confirmed":
                    return redirect('/studentapp/student_home')
                else:
                    return render(request, "guest/login.html", {"error": "Your account is pending approval. Please contact admin."})
            else:
                return render(request, "guest/login.html", {"error": "Unknown role. Please contact admin."})
        else:
            context = {"error": "Incorrect username or password"}
            return render(request, "guest/login.html",context)
    
    return render(request, "guest/login.html")



def get_batches_by_course(request):
    if request.method == 'GET':
        course_id = request.GET.get('course_id')
        
        if course_id:
            batches = tbl_batch.objects.filter(course_id=course_id).values('batch_id', 'batch_name')
            batches_list = list(batches)
            
            return JsonResponse({
                'success': True,
                'batches': batches_list
            })
    
    return JsonResponse({'success': False, 'batches': []})

def contact(request):
    return render(request, 'guest/contact.html')

