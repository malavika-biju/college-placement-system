from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, JsonResponse
from django.utils import timezone

from guestapp.models import tbl_company, tbl_login, tbl_student
from .models import tbl_district, tbl_batch, tbl_department, tbl_classtype, tbl_location, tbl_course, tbl_trainingclass, tbl_requests, tbl_student_schedule
from companyapp.models import tbl_jobpost
from django.core.paginator import Paginator
from datetime import date


def admin_dashboard(request):
    return render(request, 'Admin/index.html')


def district(request):
    # Show the district form page
    return render(request, "Admin/district.html")


def district_insert(request):
    if request.method == "POST":
        dname = request.POST.get("district_name")

        # Check duplicate
        if tbl_district.objects.filter(district_name=dname).exists():
            return HttpResponse("<script>alert('District already exists');window.location='/Admin/district';</script>")

        # Insert new district
        obj = tbl_district(district_name=dname)
        obj.save()

        return HttpResponse("<script>alert('District added successfully');window.location='/adminapp/district';</script>")

    return HttpResponse("<script>alert('Invalid Request');window.location='/adminapp/district';</script>")
def view_districts(request):
    data = tbl_district.objects.all().order_by('district_name')
    return render(request, "Admin/view_districts.html", {"districts": data})

def delete_district(request, district_id):
    try:
        district = tbl_district.objects.get(district_id=district_id)
        district.delete()
        return HttpResponse("<script>alert('District deleted successfully');window.location='/adminapp/district/view/';</script>")
    except tbl_district.DoesNotExist:
        return HttpResponse("<script>alert('District not found');window.location='/adminapp/district/view/';</script>")
    
def edit_district(request, district_id):
    try:
        district = tbl_district.objects.get(district_id=district_id)
    except tbl_district.DoesNotExist:
        return HttpResponse("<script>alert('District not found');window.location='/adminapp/district/view/';</script>")

    if request.method == "POST":
        new_name = request.POST.get("district_name")

        # Check for duplicate name excluding the current district
        if tbl_district.objects.filter(district_name=new_name).exclude(district_id=district_id).exists():
            return HttpResponse("<script>alert('District name already exists');window.location='/adminapp/edit_district/{}';</script>".format(district_id))

        district.district_name = new_name
        district.save()
        return HttpResponse("<script>alert('District updated successfully');window.location='/adminapp/district/view/';</script>")

    return render(request, "Admin/edit_district.html", {"district": district})

def batch(request):
    return render(request, "Admin/batch.html")


def batch_insert(request):
    if request.method == "POST":
        byear = request.POST.get("batch_year")

        if tbl_batch.objects.filter(batch_year=byear).exists():
            return HttpResponse("<script>alert('Batch already exists');window.location='/adminapp/batch/';</script>")

        obj = tbl_batch(batch_year=byear)
        obj.save()

        return HttpResponse("<script>alert('Batch added successfully');window.location='/adminapp/batch/';</script>")

    return HttpResponse("<script>alert('Invalid Request');window.location='/adminapp/batch/';</script>")

def view_batch(request):
    data = tbl_batch.objects.all().order_by('batch_year')
    return render(request, "Admin/view_batch.html", {"batches": data})
def delete_batch(request, batch_id):
    try:
        batch = tbl_batch.objects.get(batch_id=batch_id)
        batch.delete()
        return HttpResponse("<script>alert('Batch deleted successfully');window.location='/adminapp/view_batch/';</script>")
    except tbl_batch.DoesNotExist:
        return HttpResponse("<script>alert('Batch not found');window.location='/adminapp/view_batch/';</script>")
    
def edit_batch(request, batch_id):
    try:
        batch = tbl_batch.objects.get(batch_id=batch_id)
    except tbl_batch.DoesNotExist:
        return HttpResponse("<script>alert('Batch not found');window.location='/adminapp/view_batch/';</script>")

    if request.method == "POST":
        new_year = request.POST.get("batch_year")

        if tbl_batch.objects.filter(batch_year=new_year).exclude(batch_id=batch_id).exists():
            return HttpResponse("<script>alert('Batch year already exists');window.location='/adminapp/edit_batch/{}';</script>".format(batch_id))

        batch.batch_year = new_year
        batch.save()
        return HttpResponse("<script>alert('Batch updated successfully');window.location='/adminapp/view_batch/';</script>")

    return render(request, "Admin/edit_batch.html", {"batch": batch})



def department(request):
    return render(request, "Admin/department.html")


def department_insert(request):
    if request.method == "POST":
        name = request.POST.get("department_name")

        # Duplicate check
        if tbl_department.objects.filter(department_name=name).exists():
            return HttpResponse(
                "<script>alert('Department already exists');window.location='/adminapp/department/';</script>"
            )

        tbl_department.objects.create(department_name=name)

        return HttpResponse(
            "<script>alert('Department added successfully');window.location='/adminapp/department/';</script>"
        )

    return HttpResponse(
        "<script>alert('Invalid Request');window.location='/adminapp/department/';</script>"
    )


def view_department(request):
    data = tbl_department.objects.all().order_by("department_name")
    return render(request, "Admin/view_department.html", {"departments": data})

def delete_department(request, department_id):

    try:
        department = tbl_department.objects.get(department_id=department_id)
        department.delete()
        return HttpResponse("<script>alert('Department deleted successfully');window.location='/adminapp/view_department/';</script>")
    except tbl_department.DoesNotExist:
        return HttpResponse("<script>alert('Department not found');window.location='/adminapp/view_department/';</script>")
    
def edit_department(request, department_id):
    try:
        department = tbl_department.objects.get(department_id=department_id)
    except tbl_department.DoesNotExist:
        return HttpResponse("<script>alert('Department not found');window.location='/adminapp/view_department/';</script>")

    if request.method == "POST":
        new_name = request.POST.get("department_name")

        # Duplicate name check
        if tbl_department.objects.filter(department_name=new_name).exclude(department_id=department_id).exists():
            return HttpResponse(
                "<script>alert('Department name already exists');window.location='/adminapp/department/edit/{}/';</script>".format(
                    department_id
                )
            )

        department.department_name = new_name
        department.save()

        return HttpResponse(
            "<script>alert('Department updated successfully');window.location='/adminapp/view_department/';</script>"
        )

    return render(request, "Admin/edit_department.html", {"department": department})

def classtype(request):
    return render(request, "Admin/classtype.html")

def classtype_insert(request):
    if request.method == "POST":
        name = request.POST.get("classtype_name")

        if tbl_classtype.objects.filter(classtype_name=name).exists():
            return HttpResponse("<script>alert('Class Type already exists');window.location='/adminapp/classtype/';</script>")

        tbl_classtype.objects.create(classtype_name=name)
        return HttpResponse("<script>alert('Class Type added');window.location='/adminapp/classtype/';</script>")

    return HttpResponse("<script>alert('Invalid Request');window.location='/adminapp/classtype/';</script>")


def view_classtype(request):
    data = tbl_classtype.objects.all().order_by('classtype_name')
    return render(request, "Admin/view_classtype.html", {"classtypes": data})

def delete_classtype(request, classtype_id):
    try:
        classtype = tbl_classtype.objects.get(classtype_id=classtype_id)
        classtype.delete()
        return HttpResponse("<script>alert('Class Type deleted successfully');window.location='/adminapp/view_classtype/';</script>")
    except tbl_classtype.DoesNotExist:
        return HttpResponse("<script>alert('Class Type not found');window.location='/adminapp/view_classtype/';</script>")

def edit_classtype(request, classtype_id):
    try:
        classtype = tbl_classtype.objects.get(classtype_id=classtype_id)
    except tbl_classtype.DoesNotExist:
        return HttpResponse("<script>alert('Class Type not found');window.location='/adminapp/view_classtype/';</script>")

    if request.method == "POST":
        new_name = request.POST.get("classtype_name")

        if tbl_classtype.objects.filter(classtype_name=new_name).exclude(classtype_id=classtype_id).exists():
            return HttpResponse("<script>alert('Class Type name already exists');window.location='/adminapp/edit_classtype/{}';</script>".format(classtype_id))

        classtype.classtype_name = new_name
        classtype.save()
        return HttpResponse("<script>alert('Class Type updated successfully');window.location='/adminapp/view_classtype/';</script>")

    return render(request, "Admin/edit_classtype.html", {"classtype": classtype})

def location(request):
    districts = tbl_district.objects.all()
    return render(request, "Admin/location.html", {'districts': districts})


def location_insert(request):
    if request.method == "POST":

        district_id = request.POST.get("ddldistrict")
        location_name = request.POST.get("locname")

        # FK get
        district_obj = tbl_district.objects.get(district_id=district_id)

        # FIX: use district_id (not district)
        if tbl_location.objects.filter(location_name=location_name, district_id=district_id).exists():
            return HttpResponse("<script>alert('Location already exists');window.location='/adminapp/location/';</script>")

        # Insert
        obj = tbl_location(location_name=location_name, district_id=district_obj)
        obj.save()

        return HttpResponse("<script>alert('Location added');window.location='/adminapp/location/';</script>")

    return HttpResponse("<script>alert('Invalid Request');window.location='/adminapp/location/';</script>")


def view_location(request):
  district=tbl_district.objects.all()
  return render(request, "Admin/view_location.html", {"dis": district}) 

def filllocation(request):
    did=int(request.POST.get("did"))
    location = tbl_location.objects.filter(district_id=did).values()
    return JsonResponse(list(location), safe=False)

def delete_location(request, location_id):
    try:
        location = tbl_location.objects.get(location_id=location_id)
        location.delete()
        return HttpResponse("<script>alert('Location deleted successfully');window.location='/adminapp/view_location/';</script>")
    except tbl_location.DoesNotExist:
        return HttpResponse("<script>alert('Location not found');window.location='/adminapp/view_location/';</script>")
    
def edit_location(request, location_id):
    try:
        location = tbl_location.objects.get(location_id=location_id)
        districts = tbl_district.objects.all()
    except tbl_location.DoesNotExist:
        return HttpResponse("<script>alert('Location not found');window.location='/adminapp/view_location/';</script>")

    if request.method == "POST":
        new_name = request.POST.get("location_name")
        new_district_id = request.POST.get("district_id")  # FIXED NAME

        # FK get
        district_obj = tbl_district.objects.get(district_id=new_district_id)

        # Duplicate check
        if tbl_location.objects.filter(
            location_name=new_name,
            district_id=new_district_id
        ).exclude(location_id=location_id).exists():
            return HttpResponse(
                "<script>alert('Location already exists in this district');window.location='/adminapp/edit_location/{}/';</script>".format(location_id)
            )

        location.location_name = new_name
        location.district_id = district_obj
        location.save()

        return HttpResponse("<script>alert('Location updated successfully');window.location='/adminapp/view_location/';</script>")

    return render(request, "Admin/edit_location.html", {"location": location, "districts": districts})

def course(request):
    departments = tbl_department.objects.all()
    return render(request, "Admin/course.html", {"departments": departments})

def course_insert(request):
    if request.method == "POST":
        name = request.POST.get("course_name")
        dept_id = request.POST.get("department_id")

        dept_obj = tbl_department.objects.get(department_id=dept_id)

        if tbl_course.objects.filter(course_name=name, department_id=dept_obj).exists():
            return HttpResponse("<script>alert('Course already exists');window.location='/adminapp/course/';</script>")

        tbl_course.objects.create(course_name=name, department_id=dept_obj)
        return HttpResponse("<script>alert('Course added successfully');window.location='/adminapp/course/';</script>")

    return HttpResponse("<script>alert('Invalid Request');window.location='/adminapp/course/';</script>")
def view_course(request):
    data = tbl_department.objects.all()
    return render(request, "Admin/view_course.html", {"dept": data})

def fillcourse(request):
    did=int(request.POST.get("did"))
    course = tbl_course.objects.filter(department_id=did).values()
    return JsonResponse(list(course), safe=False)

def delete_course(request, course_id):
    try:
        course = tbl_course.objects.get(course_id=course_id)
        course.delete()
        return HttpResponse("<script>alert('Course deleted successfully');window.location='/adminapp/view_course/';</script>")
    except tbl_course.DoesNotExist:
        return HttpResponse("<script>alert('Course not found');window.location='/adminapp/view_course/';</script>")
    
def edit_course(request, course_id):
    try:
        course = tbl_course.objects.get(course_id=course_id)
        departments = tbl_department.objects.all()
    except tbl_course.DoesNotExist:
        return HttpResponse("<script>alert('Course not found');window.location='/adminapp/view_course/';</script>")

    if request.method == "POST":
        new_name = request.POST.get("course_name")
        new_department_id = request.POST.get("department_id")

        dept_obj = tbl_department.objects.get(department_id=new_department_id)

        if tbl_course.objects.filter(
            course_name=new_name,
            department_id=dept_obj
        ).exclude(course_id=course_id).exists():
            return HttpResponse(
                "<script>alert('Course already exists in this department');window.location='/adminapp/edit_course/{}/';</script>".format(course_id)
            )

        course.course_name = new_name
        course.department_id = dept_obj
        course.save()

        return HttpResponse("<script>alert('Course updated successfully');window.location='/adminapp/view_course/';</script>")

    return render(request, "Admin/edit_course.html", {"course": course, "departments": departments})

def trainingclass(request):
    batches = tbl_batch.objects.all()
    classtypes = tbl_classtype.objects.all()
      
    courses = tbl_course.objects.all()
    districts = tbl_district.objects.all()
    departments = tbl_department.objects.all()


    
    return render(request, "Admin/trainingclass.html", {
        "batches": batches,
        "classtypes": classtypes,
       
        "courses": courses,
        "districts": districts,
        "departments": departments,

    })

def training_class_insert(request):
    if request.method == "POST":
        tname = request.POST.get("trainingclass_name")
        stime = request.POST.get("start_time")
        tdate = request.POST.get("date")
        course_id = request.POST.get("course_id")
        classtype_id = request.POST.get("classtype_id")
        batch_id = request.POST.get("batch_id")
        
        desc = request.POST.get("description")

        course_obj = tbl_course.objects.get(course_id=course_id)
        classtype_obj = tbl_classtype.objects.get(classtype_id=classtype_id)
        batch_obj = tbl_batch.objects.get(batch_id=batch_id)
        

        tbl_trainingclass.objects.create(
            trainingclass_name=tname,
            start_time=stime,
            date=tdate,
            course_id=course_obj,
            classtype_id=classtype_obj,
            batch_id=batch_obj,
        
            description=desc
        )

        return HttpResponse("<script>alert('Training Class added successfully');window.location='/adminapp/trainingclass/';</script>")

    return HttpResponse("<script>alert('Invalid Request');window.location='/adminapp/trainingclass/';</script>")

def view_trainingclass(request):
    departments = tbl_department.objects.all()
    courses = tbl_course.objects.all()
    return render(request, "Admin/view_trainingclass.html", {
        "departments": departments,
        "courses": courses
    })

def filltraining(request):
    cid=int(request.POST.get("cid"))
    trainingclasses = tbl_trainingclass.objects.filter(course_id=cid).values('trainingclass_id', 'trainingclass_name', 'start_time', 'date', 'description', 'batch_id__batch_year', 'classtype_id__classtype_name')
    return JsonResponse(list(trainingclasses), safe=False)

def delete_training(request, trainingclass_id):
    try:
        trainingclass = tbl_trainingclass.objects.get(trainingclass_id=trainingclass_id)
        trainingclass.delete()
        return HttpResponse("<script>alert('Training Class deleted successfully');window.location='/adminapp/view_trainingclass/';</script>")    
    except tbl_trainingclass.DoesNotExist:
        return HttpResponse("<script>alert('Training Class not found');window.location='/adminapp/view_trainingclass/';</script>")
    
def edit_training(request, trainingclass_id):
    try:
        trainingclass = tbl_trainingclass.objects.get(trainingclass_id=trainingclass_id)
        batches = tbl_batch.objects.all()
        classtypes = tbl_classtype.objects.all()
        courses = tbl_course.objects.all()
    except tbl_trainingclass.DoesNotExist:
        return HttpResponse("<script>alert('Training Class not found');window.location='/adminapp/view_trainingclass/';</script>")

    if request.method == "POST":
        new_name = request.POST.get("trainingclass_name")
        new_start_time = request.POST.get("start_time")
        new_date = request.POST.get("date")
        new_course_id = request.POST.get("course_id")
        new_classtype_id = request.POST.get("classtype_id")
        new_batch_id = request.POST.get("batch_id")
        new_description = request.POST.get("description")

        course_obj = tbl_course.objects.get(course_id=new_course_id)
        classtype_obj = tbl_classtype.objects.get(classtype_id=new_classtype_id)
        batch_obj = tbl_batch.objects.get(batch_id=new_batch_id)

        trainingclass.trainingclass_name = new_name
        trainingclass.start_time = new_start_time
        trainingclass.date = new_date
        trainingclass.course_id = course_obj
        trainingclass.classtype_id = classtype_obj
        trainingclass.batch_id = batch_obj
        trainingclass.description = new_description
        trainingclass.save()

        return HttpResponse("<script>alert('Training Class updated successfully');window.location='/adminapp/view_trainingclass/';</script>")

    return render(request, "Admin/edit_training.html", {
        "trainingclass": trainingclass,
        "batches": batches,
        "classtypes": classtypes,
        "courses": courses
    })

def view_company(request):
    companies = tbl_company.objects.filter(login_id__status='requested').order_by('company_name')
    return render(request, "Admin/view_company.html", {"companies": companies})

def accept_company(request,loginid):
    login = tbl_login.objects.get(login_id=loginid)
    login.status = 'confirmed'
    login.save()
    return admin_dashboard(request)

def reject_company(request,loginid):
    login = tbl_login.objects.get(login_id=loginid)
    login.status = 'rejected'
    login.save()
    return admin_dashboard(request)

def view_student(request):
    """View all students with their details"""
    # Filter by status if requested
    status = request.GET.get('status', 'requested')
    
    # Get students with their login details
    students = tbl_student.objects.select_related(
        'login_id', 
        'course_id', 
        'batch_id'
    ).order_by('student_name')
    
    # Filter by login status
    if status == 'confirmed':
        students = students.filter(login_id__status='confirmed')
    elif status == 'rejected':
        students = students.filter(login_id__status='rejected')
    else:  # requested (default)
        students = students.filter(login_id__status='requested')
    
    # Calculate counts for different statuses
    total_students = tbl_student.objects.count()
    confirmed_count = tbl_student.objects.filter(login_id__status='confirmed').count()
    requested_count = tbl_student.objects.filter(login_id__status='requested').count()
    rejected_count = tbl_student.objects.filter(login_id__status='rejected').count()
    
    context = {
        'students': students,
        'status_filter': status,
        'total_students': total_students,
        'confirmed_count': confirmed_count,
        'requested_count': requested_count,
        'rejected_count': rejected_count,
    }
    return render(request, "Admin/view_student.html", context)


def accept_student(request, loginid):
    """Accept a student registration"""
    try:
        login = tbl_login.objects.get(login_id=loginid)
        login.status = 'confirmed'
        login.save()
        
        return HttpResponse("<script>alert('Student accepted successfully');window.location='/adminapp/view_student/';</script>")
    except tbl_login.DoesNotExist:
        return HttpResponse("<script>alert('Student not found');window.location='/adminapp/view_student/';</script>")


def reject_student(request, loginid):
    """Reject a student registration"""
    try:
        login = tbl_login.objects.get(login_id=loginid)
        login.status = 'rejected'
        login.save()
        
        return HttpResponse("<script>alert('Student rejected successfully');window.location='/adminapp/view_student/';</script>")
    except tbl_login.DoesNotExist:
        return HttpResponse("<script>alert('Student not found');window.location='/adminapp/view_student/';</script>")

# Add these views to your views.py

def view_job_posts(request):
    """View all job posts with filters"""
    try:
        # Get all job posts - SIMPLIFIED without select_related for now
        jobposts_list = tbl_jobpost.objects.all().order_by('-post_date')
        
        print(f"DEBUG: Found {jobposts_list.count()} jobs in database")
        
        # Check if we get the data
        if jobposts_list.exists():
            for job in jobposts_list:
                print(f"Job ID: {job.jobpost_id}, Position: {job.position}")
        
        # Apply filters if needed
        status_filter = request.GET.get('status', '')
        if status_filter:
            jobposts_list = jobposts_list.filter(status=status_filter)
        
        search_query = request.GET.get('search', '')
        if search_query:
            jobposts_list = jobposts_list.filter(position__icontains=search_query)
        
        # Pagination
        paginator = Paginator(jobposts_list, 10)
        page_number = request.GET.get('page')
        jobposts = paginator.get_page(page_number)
        
        # Get companies for dropdown
        companies = tbl_company.objects.filter(login_id__status='confirmed')
        
        # Get today's date
        today = date.today()
        print(f"DEBUG: Today is {today}")
        
        context = {
            'jobposts': jobposts,
            'status_filter': status_filter,
            'company_filter': '',
            'search_query': search_query,
            'companies': companies,
            'today': today,
        }
        return render(request, "Admin/view_job_posts.html", context)
        
    except Exception as e:
        print(f"ERROR in view_job_posts: {str(e)}")
        import traceback
        traceback.print_exc()
        
        # Return a simple error message
        return HttpResponse(f"""
            <h1>Error loading job posts</h1>
            <p>Error: {str(e)}</p>
            <p><a href="/adminapp/admin_dashboard/">Back to Dashboard</a></p>
        """)

def job_details(request, jobpost_id):
    """View detailed information about a specific job post"""
    try:
        jobpost = tbl_jobpost.objects.select_related('company_id').get(jobpost_id=jobpost_id)
        
        # Get company details
        company = jobpost.company_id
        
        # Count total students in system (optional)
        total_students = tbl_student.objects.filter(login_id__status='confirmed').count()
        
        # Check if job is expired
        today = date.today()
        is_expired = jobpost.application_end_date < today
        
        context = {
            'jobpost': jobpost,
            'company': company,
            'total_students': total_students,
            'today': today,
            'is_expired': is_expired,
        }
        return render(request, "Admin/job_details.html", context)
        
    except tbl_jobpost.DoesNotExist:
        return HttpResponse(
            "<script>alert('Job post not found');window.location='/adminapp/job_posts/';</script>"
        )
def view_students_for_job(request, jobpost_id):
    """View students who meet the job requirements"""
    try:
        # Get job post
        jobpost = tbl_jobpost.objects.get(jobpost_id=jobpost_id)
        
        # Debug print
        print(f"DEBUG: Found jobpost - ID: {jobpost.jobpost_id}, Position: {jobpost.position}, Cutoff: {jobpost.cutoff_mark}")
        
        # Get all departments, batches, and courses
        department = tbl_department.objects.all()
        batch = tbl_batch.objects.all()
        courses = tbl_course.objects.all()
        
        # Get filter parameters from GET request
        selected_department = request.GET.get('department', '')
        selected_batch = request.GET.get('batch', '')
        selected_course = request.GET.get('course', '')
        
        # Start with all confirmed students
        students = tbl_student.objects.filter(
            login_id__status='confirmed'
        ).select_related('course_id', 'batch_id', 'course_id__department_id')
        
        # Debug: Count all confirmed students
        print(f"DEBUG: Total confirmed students: {students.count()}")
        
        # Apply filters
        if selected_department:
            students = students.filter(course_id__department_id=selected_department)
            print(f"DEBUG: After department filter: {students.count()}")
        
        if selected_batch:
            students = students.filter(batch_id=selected_batch)
            print(f"DEBUG: After batch filter: {students.count()}")
        
        if selected_course:
            students = students.filter(course_id=selected_course)
            print(f"DEBUG: After course filter: {students.count()}")
        
        # Calculate statistics
        meets_cutoff_count = 0
        below_cutoff_count = 0
        
        # IMPORTANT FIX: Create a list to store student data with meets_cutoff flag
        students_with_eligibility = []
        
        for student in students:
            student_score = student.percentage if student.percentage else 0
            meets_cutoff = student_score >= jobpost.cutoff_mark
            
            # Store student data in a dictionary
            student_data = {
                'student': student,
                'meets_cutoff': meets_cutoff,
                'percentage': student_score,
            }
            students_with_eligibility.append(student_data)
            
            if meets_cutoff:
                meets_cutoff_count += 1
            else:
                below_cutoff_count += 1
            
            # Debug for first few students
            if len(students_with_eligibility) <= 3:
                print(f"DEBUG: Student {student.student_name} - Score: {student_score}, Cutoff: {jobpost.cutoff_mark}, Meets: {meets_cutoff}")
        
        print(f"DEBUG: Meets cutoff: {meets_cutoff_count}, Below cutoff: {below_cutoff_count}")
        
        context = {
            'jobpost': jobpost,
            'company': jobpost.company_id,
            'students_data': students_with_eligibility,  # Changed to students_data
            'department': department,
            'batch': batch,
            'courses': courses,
            'total_students': len(students_with_eligibility),
            'meets_cutoff_count': meets_cutoff_count,
            'below_cutoff_count': below_cutoff_count,
            'selected_department': selected_department,
            'selected_batch': selected_batch,
            'selected_course': selected_course,
        }
        return render(request, "Admin/view_students_for_job.html", context)
        
    except tbl_jobpost.DoesNotExist:
        print(f"DEBUG: Job post not found - ID: {jobpost_id}")
        return HttpResponse(
            "<script>alert('Job post not found');window.location='/adminapp/job_posts/';</script>"
        )
    except Exception as e:
        print(f"DEBUG: Error in view_students_for_job: {str(e)}")
        return HttpResponse(
            f"<script>alert('Error: {str(e)}');window.location='/adminapp/job_posts/';</script>"
        )
def get_courses_by_department(request):
    """Get courses by department (AJAX)"""
    if request.method == "POST":
        department_id = request.POST.get('did')
        if department_id:
            courses = tbl_course.objects.filter(department_id=department_id).values('course_id', 'course_name')
            return JsonResponse(list(courses), safe=False)
    return JsonResponse([], safe=False)

def get_all_courses(request):
    """Get all courses (AJAX)"""
    if request.method == "POST":
        courses = tbl_course.objects.all().values('course_id', 'course_name')
        return JsonResponse(list(courses), safe=False)
    return JsonResponse([], safe=False)

def request_company(request):
    """Create and send a request to company"""
    if request.method == "POST":
        try:
            # Get form data
            jobpost_id = request.POST.get('jobpost_id')
            batch_id = request.POST.get('batch_id')
            course_id = request.POST.get('course_id')
            student_count = request.POST.get('student_count')
            send_all = request.POST.get('send_all', 'false')
            
            # Set status based on send_all
            status = 'pending'
            if send_all == 'true':
                status = 'bulk_pending'
            
            print(f"DEBUG: Creating request for JobPost {jobpost_id}")
            print(f"DEBUG: Batch: {batch_id}, Course: {course_id}")
            print(f"DEBUG: Student count: {student_count}, Status: {status}, Send All: {send_all}")
            
            # Validate required fields
            if not jobpost_id or not batch_id or not course_id or not student_count:
                return HttpResponse(
                    "<script>alert('Please fill all required fields');window.location='/adminapp/view_students_for_job/{}/';</script>".format(jobpost_id)
                )
            
            # Get related objects
            jobpost = tbl_jobpost.objects.get(jobpost_id=jobpost_id)
            batch = tbl_batch.objects.get(batch_id=batch_id)
            course = tbl_course.objects.get(course_id=course_id)
            
            # Create the request record - USING tbl_requests (with 's')
            request_obj = tbl_requests.objects.create(
                jobpost_id=jobpost,  # This is the ForeignKey
                batch_id=batch,
                student_count=int(student_count),
                course_id=course,
                status=status
                # request_date is auto_now_add=True, so it will be set automatically
            )
            
            print(f"DEBUG: Created request #{request_obj.request_id}")
            
            return HttpResponse(
                f"""
                <script>
                    alert('Request #{request_obj.request_id} created successfully!\\n\\n'
                          + 'Details:\\n'
                          + '- Job: {jobpost.position}\\n'
                          + '- Company: {jobpost.company_id.company_name}\\n'
                          + '- Date: {request_obj.request_date}\\n'
                          + '- Batch: {batch.batch_year}\\n'
                          + '- Course: {course.course_name}\\n'
                          + '- Students: {student_count}\\n'
                          + '- Status: {status}\\n'
                          + '- Type: {"All Eligible Students" if send_all == "true" else "Filtered Students"}\\n\\n'
                          + 'Request has been sent to {jobpost.company_id.company_name}.');
                    window.location='/adminapp/job_posts/';
                </script>
                """
            )
            
        except Exception as e:
            print(f"DEBUG: Error in request_company: {str(e)}")
            import traceback
            traceback.print_exc()
            jobpost_id = request.POST.get('jobpost_id', '')
            return HttpResponse(
                f"""
                <script>
                    alert('Error: {str(e)}');
                    window.location='/adminapp/view_students_for_job/{jobpost_id}/';
                </script>
                """
            )
    
    return HttpResponse(
        "<script>alert('Invalid request');window.location='/adminapp/job_posts/';</script>"
    )
def request_company_approval(request, jobpost_id):
    """Send selected students to company"""
    if request.method == "POST":
        try:
            jobpost = tbl_jobpost.objects.get(jobpost_id=jobpost_id)
            selected_students = request.POST.get('selected_students', '')
            student_count = request.POST.get('student_count', 0)
            message = request.POST.get('message', '')
            
            print(f"DEBUG: Sending {student_count} students to company")
            print(f"DEBUG: Selected students IDs: {selected_students}")
            print(f"DEBUG: Message: {message}")
            
            # TODO: Here you would typically:
            # 1. Create a record in a new model (e.g., JobApplication)
            # 2. Send email notification to company
            # 3. Update job post status if needed
            
            return HttpResponse(
                f"""
                <script>
                    alert('Successfully sent {student_count} student(s) to {jobpost.company_id.company_name} for approval.');
                    window.location='/adminapp/job_posts/';
                </script>
                """
            )
            
        except Exception as e:
            print(f"DEBUG: Error in request_company_approval: {str(e)}")
            return HttpResponse(
                f"""
                <script>
                    alert('Error: {str(e)}');
                    window.location='/adminapp/view_students_for_job/{jobpost_id}/';
                </script>
                """
            )
    
    return HttpResponse(
        "<script>alert('Invalid request');window.location='/adminapp/job_posts/';</script>"
    )


# Add this to your adminapp/views.py
def view_company_accepted_students(request):
    """View requests approved by companies and the students who meet criteria"""
    try:
        # Get all approved requests
        approved_requests = tbl_requests.objects.filter(
            status='approved'
        ).select_related(
            'jobpost_id',
            'jobpost_id__company_id',
            'batch_id',
            'course_id'
        ).order_by('-request_date')
        
        # Get all confirmed companies
        companies = tbl_company.objects.filter(login_id__status='confirmed')
        
        # Get filter parameters
        company_filter = request.GET.get('company', '')
        batch_filter = request.GET.get('batch', '')
        course_filter = request.GET.get('course', '')
        
        # Apply filters
        if company_filter:
            approved_requests = approved_requests.filter(jobpost_id__company_id=company_filter)
        
        if batch_filter:
            approved_requests = approved_requests.filter(batch_id=batch_filter)
        
        if course_filter:
            approved_requests = approved_requests.filter(course_id=course_filter)
        
        # Get all batches and courses for filters
        batches = tbl_batch.objects.all()
        courses = tbl_course.objects.all()
        
        # Get job posts for reference
        job_posts = tbl_jobpost.objects.all()
        
        # Prepare data for each approved request
        request_data = []
        for req in approved_requests:
            # Get students who meet the criteria for this request
            students = tbl_student.objects.filter(
                login_id__status='confirmed',
                batch_id=req.batch_id,
                course_id=req.course_id
            )
            
            # Check if students meet cutoff
            eligible_students = []
            for student in students:
                student_score = student.percentage if student.percentage else 0
                meets_cutoff = student_score >= req.jobpost_id.cutoff_mark
                
                if meets_cutoff:
                    eligible_students.append({
                        'student': student,
                        'percentage': student_score,
                    })
            
            # Calculate statistics for this request
            total_students = students.count()
            eligible_count = len(eligible_students)
            
            request_data.append({
                'request': req,
                'company': req.jobpost_id.company_id,
                'jobpost': req.jobpost_id,
                'total_students': total_students,
                'eligible_students': eligible_students,
                'eligible_count': eligible_count,
                'requested_count': req.student_count,
            })
        
        # Calculate overall statistics
        total_approved_requests = approved_requests.count()
        total_eligible_students = sum(item['eligible_count'] for item in request_data)
        
        context = {
            'request_data': request_data,
            'companies': companies,
            'batches': batches,
            'courses': courses,
            'job_posts': job_posts,
            'company_filter': company_filter,
            'batch_filter': batch_filter,
            'course_filter': course_filter,
            'total_approved_requests': total_approved_requests,
            'total_eligible_students': total_eligible_students,
        }
        
        return render(request, "Admin/company_accepted_students.html", context)
        
    except Exception as e:
        print(f"Error in view_company_accepted_students: {str(e)}")
        return HttpResponse(
            f"""
            <script>
                alert('Error loading accepted students: {str(e)}');
                window.location='/adminapp/admin_dashboard/';
            </script>
            """
        )

def view_company_accepted_students(request):
    """View students accepted by companies based on approved requests"""
    try:
        # Get today's date for comparisons
        today = date.today()
        
        # Get all approved requests
        approved_requests = tbl_requests.objects.filter(
            status='approved'
        ).select_related(
            'jobpost_id',
            'jobpost_id__company_id',
            'batch_id',
            'course_id'
        ).order_by('-request_date')
        
        
        companies = tbl_company.objects.filter(login_id__status='confirmed').order_by('company_name')
        
        # Get filter parameters from GET request
        company_filter = request.GET.get('company', '')
        batch_filter = request.GET.get('batch', '')
        course_filter = request.GET.get('course', '')
        
        # Apply filters
        if company_filter:
            approved_requests = approved_requests.filter(jobpost_id__company_id=company_filter)
        
        if batch_filter:
            approved_requests = approved_requests.filter(batch_id=batch_filter)
        
        if course_filter:
            approved_requests = approved_requests.filter(course_id=course_filter)
        
        # Get all batches and courses for filter dropdowns
        batches = tbl_batch.objects.all().order_by('batch_year')
        courses = tbl_course.objects.all().order_by('course_name')
        
        # Prepare data for each approved request
        request_data = []
        for req in approved_requests:
            try:
                # Get all confirmed students for this batch and course
                students = tbl_student.objects.filter(
                    login_id__status='confirmed',
                    batch_id=req.batch_id,
                    course_id=req.course_id
                )
                
                # Check if students meet the cutoff mark
                eligible_students = []
                for student in students:
                    # Safely get percentage (handle None values)
                    student_score = student.percentage if student.percentage else 0
                    cutoff_mark = req.jobpost_id.cutoff_mark if req.jobpost_id.cutoff_mark else 0
                    
                    meets_cutoff = student_score >= cutoff_mark
                    
                    if meets_cutoff:
                        eligible_students.append({
                            'student': student,
                            'percentage': student_score,
                        })
                
                # Get total students count for this batch/course combination
                total_students = students.count()
                eligible_count = len(eligible_students)
                
                # Safely get requested count
                requested_count = req.student_count if req.student_count else 0
                
                request_data.append({
                    'request': req,
                    'company': req.jobpost_id.company_id,
                    'jobpost': req.jobpost_id,
                    'total_students': total_students,
                    'eligible_students': eligible_students,
                    'eligible_count': eligible_count,
                    'requested_count': requested_count,
                })
                
            except Exception as e:
                print(f"Error processing request {req.request_id}: {str(e)}")
                # Skip this request if there's an error
                continue
        
        # Calculate overall statistics
        total_approved_requests = len(request_data)
        total_eligible_students = sum(item['eligible_count'] for item in request_data)
        
        context = {
            'request_data': request_data,
            'companies': companies,
            'batches': batches,
            'courses': courses,
            'company_filter': company_filter,
            'batch_filter': batch_filter,
            'course_filter': course_filter,
            'total_approved_requests': total_approved_requests,
            'total_eligible_students': total_eligible_students,
            'today': today,  # Pass today's date for template comparisons
        }
        
        return render(request, "Admin/company_accepted_students.html", context)
        
    except Exception as e:
        print(f"Error in view_company_accepted_students: {str(e)}")
        import traceback
        traceback.print_exc()
        
        # Show error message
        return HttpResponse(
            f"""
            <script>
                alert('Error loading accepted students: {str(e)}');
                window.location='/adminapp/admin_dashboard/';
            </script>
            """
        )
    
def interview_schedule(request, id):
    schedule = tbl_requests.objects.get(request_id=id)
    students = tbl_student.objects.filter(batch_id=schedule.batch_id, course_id=schedule.course_id)
    return render(request, "admin/interview_schedule.html", {'student': schedule, 'students': students})

def assign_students(request):
    if request.method == "POST":
        request_id = request.POST.get('request_id')
        selected_students = request.POST.getlist('selected_students')
        
        try:
            req = tbl_requests.objects.get(request_id=request_id)
            
            for student_id in selected_students:
                student = tbl_student.objects.get(student_id=student_id)
                
                tbl_student_schedule.objects.create(
                    student_id=student,
                    request_id=req,
                    status='assigned'
                )
            
            return HttpResponse("<script>alert('Students assigned successfully');window.location='/adminapp/company_accepted_students/';</script>")
        except Exception as e:
            print(f"Error: {str(e)}")
            return HttpResponse(f"<script>alert('Error: {str(e)}');window.location='/adminapp/company_accepted_students/';</script>")
    
    return HttpResponse("<script>alert('Invalid request');window.location='/adminapp/company_accepted_students/';</script>")