from django.shortcuts import redirect, render
from guestapp.models import tbl_student
from adminapp.models import tbl_interview_schedule, tbl_student_schedule, tbl_trainingclass
from datetime import date

def student_home(request):
    return render(request, 'student/index.html')

def resume(request):
    return render(request, 'student/resume.html')

def student_trainingclass(request):
    if 'login_id' not in request.session:
        return redirect('/login')
    
    login_id = request.session['login_id']
    
    try:
        student = tbl_student.objects.get(login_id=login_id)
        
        training_classes = tbl_trainingclass.objects.filter(
            course_id=student.course_id,
            batch_id=student.batch_id
        ).order_by('date', 'start_time')
        
        today = date.today()
        
        status = request.GET.get('status', 'all')
        if status == 'upcoming':
            training_classes = training_classes.filter(date__gte=today)
        elif status == 'past':
            training_classes = training_classes.filter(date__lt=today)
        
        search_query = request.GET.get('search', '')
        if search_query:
            training_classes = training_classes.filter(
                trainingclass_name__icontains=search_query
            ) | training_classes.filter(
                description__icontains=search_query
            )
        
        context = {
            'student': student,
            'training_classes': training_classes,
            'total_classes': training_classes.count(),
            'today': today,
            'status_filter': status,
            'search_query': search_query
        }
        
        return render(request, 'student/student_trainingclass.html', context)
        
    except tbl_student.DoesNotExist:
        request.session.flush()
        return render(request, 'guest/login.html', {'error': 'Student profile not found. Please login again.'})

def student_accepted_jobs(request):
    if 'login_id' not in request.session:
        return redirect('/login')
    
    login_id = request.session['login_id']
    
    try:
        student = tbl_student.objects.get(login_id=login_id)
        
        accepted_applications = tbl_student_schedule.objects.filter(
            student_id=student,
            status='assigned'
        ).select_related(
            'request_id',
            'request_id__jobpost_id',
            'request_id__jobpost_id__company_id',
            'schedule_id'
        ).order_by('-request_id__request_date')
        
        upcoming_interviews = []
        for app in accepted_applications:
            if app.schedule_id and app.schedule_id.schedule_date >= date.today():
                upcoming_interviews.append(app)
        
        context = {
            'student': student,
            'accepted_applications': accepted_applications,
            'upcoming_interviews': upcoming_interviews,
            'today': date.today(),
        }
        
        return render(request, "student/student_accepted_jobs.html", context)
        
    except tbl_student.DoesNotExist:
        request.session.flush()
        return render(request, 'guest/login.html', {'error': 'Student profile not found. Please login again.'})