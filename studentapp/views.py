from django.shortcuts import redirect, render
from guestapp.models import tbl_student
from adminapp.models import tbl_interview_schedule, tbl_student_schedule, tbl_trainingclass
from datetime import date
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.cache import cache_control


@cache_control(no_cache=True, must_revalidate=True, no_store=True)

def student_home(request):
    logid = request.session.get('login_id')
    if logid:
        return render(request, 'student/index.html')
    else:
        return HttpResponse("<script>alert('Authenication Required Please login page');window.location='/guestapp/guest_home';</script>")
@cache_control(no_cache=True, must_revalidate=True, no_store=True)

def logout_view(request):
    logid = request.session.get('login_id')
    if logid:
        return render(request, 'student/index.html')
    else:
        return HttpResponse("<script>alert('Authenication Required Please login page');window.location='/guestapp/guest_home';</script>")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def student_trainingclass(request):
    logid = request.session.get('login_id')
    if logid:

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
    else:
        return HttpResponse("<script>alert('Authenication Required Please login page');window.location='/guestapp/guest_home';</script>")
@cache_control(no_cache=True, must_revalidate=True, no_store=True)

def student_accepted_jobs(request):
    logid = request.session.get('login_id')
    if logid:
        if 'login_id' not in request.session:
            return redirect('/login')
        
        login_id = request.session['login_id']
        
        try:
            student = tbl_student.objects.get(login_id=login_id)
            
            # Get all student schedules for this student (including rejected ones)
            all_student_schedules = tbl_student_schedule.objects.filter(
                student_id=student
            ).select_related(
                'request_id',
                'request_id__jobpost_id',
                'request_id__jobpost_id__company_id',
                'schedule_id'
            ).order_by('-request_id__request_date')
            
            # Get accepted applications (status='assigned')
            accepted_applications = all_student_schedules.filter(status='assigned')
            
            # Get all scheduled interviews for this student
            scheduled_interviews = []
            for schedule in all_student_schedules:
                if schedule.schedule_id:
                    scheduled_interviews.append(schedule.schedule_id)
            
            # Remove duplicates (same interview schedule might appear multiple times)
            scheduled_interviews = list(set(scheduled_interviews))
            
            # Get upcoming interviews
            upcoming_interviews = []
            for interview in scheduled_interviews:
                if interview.schedule_date >= date.today():
                    upcoming_interviews.append(interview)
            
            # Get all interview stages for each request
            interview_stages = {}
            for schedule in all_student_schedules:
                if schedule.request_id and schedule.schedule_id:
                    request_id = schedule.request_id.request_id
                    if request_id not in interview_stages:
                        interview_stages[request_id] = []
                    interview_stages[request_id].append({
                        'stage': schedule.schedule_id.stage,
                        'date': schedule.schedule_id.schedule_date,
                        'status': schedule.status,
                        'job_position': schedule.request_id.jobpost_id.position,
                        'company': schedule.request_id.jobpost_id.company_id.company_name
                    })
            
            context = {
                'student': student,
                'accepted_applications': accepted_applications,
                'upcoming_interviews': upcoming_interviews,
                'interview_stages': interview_stages,
                'today': date.today(),
            }
            
            return render(request, "student/student_accepted_jobs.html", context)
            
        except tbl_student.DoesNotExist:
            request.session.flush()
            return render(request, 'guest/login.html', {'error': 'Student profile not found. Please login again.'})
    else:
        return HttpResponse("<script>alert('Authenication Required Please login page');window.location='/guestapp/guest_home';</script>")
@cache_control(no_cache=True, must_revalidate=True, no_store=True)

def myprofile(request):
    logid = request.session.get('login_id')
    if logid:
        if 'login_id' not in request.session:
            return redirect('/login')
        
        login_id = request.session['login_id']
        
        try:
            student = tbl_student.objects.get(login_id=login_id)
            
            context = {
                'student': student,
            }
            
            return render(request, 'student/myprofile.html', context)
            
        except tbl_student.DoesNotExist:
            request.session.flush()
            return render(request, 'guest/login.html', {'error': 'Student profile not found. Please login again.'})
    else:
        return HttpResponse("<script>alert('Authenication Required Please login page');window.location='/guestapp/guest_home';</script>")
@cache_control(no_cache=True, must_revalidate=True, no_store=True)

def update_profile(request):
    logid = request.session.get('login_id')
    if logid:
        if 'login_id' not in request.session:
            return redirect('/login')
        
        login_id = request.session['login_id']
        
        try:
            student = tbl_student.objects.get(login_id=login_id)
            
            if request.method == 'POST':
                student.student_name = request.POST.get('student_name')
                student.email = request.POST.get('email')
                student.contact_number = request.POST.get('contact_number')
                student.gender = request.POST.get('gender')
                
                percentage = request.POST.get('percentage')
                if percentage:
                    student.percentage = float(percentage)
                
                student.mark = request.POST.get('mark')
                
                if 'photo' in request.FILES:
                    student.photo = request.FILES['photo']
                
                if 'resume' in request.FILES:
                    student.resume = request.FILES['resume']
                
                if 'id_proof' in request.FILES:
                    student.id_proof = request.FILES['id_proof']
                
                student.save()
                return redirect('myprofile')
                
        except:
            return redirect('/login')
        
        return redirect('myprofile')
    else:
        return HttpResponse("<script>alert('Authenication Required Please login page');window.location='/guestapp/guest_home';</script>")
@cache_control(no_cache=True, must_revalidate=True, no_store=True)

def resume(request):
    logid = request.session.get('login_id')
    if logid:
        if 'login_id' not in request.session:
            return redirect('/login')
        
        login_id = request.session['login_id']
        
        try:
            student = tbl_student.objects.get(login_id=login_id)
            
            context = {
                'student': student,
            }
            
            return render(request, 'student/resume.html', context)
            
        except tbl_student.DoesNotExist:
            request.session.flush()
            return render(request, 'guest/login.html', {'error': 'Student profile not found. Please login again.'})
    else:
        return HttpResponse("<script>alert('Authenication Required Please login page');window.location='/guestapp/guest_home';</script>")