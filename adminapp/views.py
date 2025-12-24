from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import tbl_district, tbl_batch, tbl_department, tbl_classtype, tbl_location, tbl_course, tbl_trainingclass

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
