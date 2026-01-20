from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from .models import tbl_jobpost              
from adminapp.models import tbl_requests, tbl_student_schedule, tbl_interview_schedule
from guestapp.models import tbl_company, tbl_student

def company_home(request):
    return render(request, 'company/index.html')

def jobpost(request):
    return render(request, 'company/jobpost.html')

def jobpost_insert(request):
    if request.method == "POST":
        jobpost = tbl_jobpost()
        jobpost.requirement = request.POST.get("requirement")
        jobpost.cutoff_mark = request.POST.get("cutoff_mark")
        jobpost.application_end_date = request.POST.get("application_end_date")
        jobpost.position = request.POST.get("position")
        jobpost.photo = request.FILES.get("photo")
        company_id = tbl_company.objects.get(login_id=request.session['login_id']) 
        jobpost.company_id = company_id
        jobpost.status = "open"
        jobpost.save()
        return HttpResponse("<script>alert('Job Posted Successfully');window.location='/company_home/';</script>")
    else:
        return HttpResponse("<script>alert('Invalid Request');window.location='/jobpost/';</script>")
    
def view_jobpost(request):
    company_id = tbl_company.objects.get(login_id=request.session['login_id']) 
    jobposts = tbl_jobpost.objects.filter(company_id=company_id)
    return render(request, 'company/view_jobpost.html', {'jobposts': jobposts})

def edit_job(request, jobpost_id):
    try:
        jobpost = tbl_jobpost.objects.get(jobpost_id=jobpost_id)
    except tbl_jobpost.DoesNotExist:
        return HttpResponse("<script>alert('Job Post Not Found');window.location='/view_jobpost/';</script>")
    
    if request.method == "POST":
        jobpost.requirement = request.POST.get("requirement")
        jobpost.cutoff_mark = request.POST.get("cutoff_mark")
        jobpost.application_end_date = request.POST.get("application_end_date")
        jobpost.position = request.POST.get("position")
        if 'photo' in request.FILES:
            jobpost.photo = request.FILES.get("photo")
        jobpost.save()
        return HttpResponse("<script>alert('Job Post Updated Successfully');window.location='/view_jobpost/';</script>")
    else:
        return render(request, 'company/edit_job.html', {'jobpost': jobpost})
    
def delete_job(request, jobpost_id):
    try:
        jobpost = tbl_jobpost.objects.get(jobpost_id=jobpost_id)
        jobpost.delete()
        return HttpResponse("<script>alert('Job Post Deleted Successfully');window.location='/view_jobpost/';</script>")
    except tbl_jobpost.DoesNotExist:
        return HttpResponse("<script>alert('Job Post Not Found');window.location='/view_jobpost/';</script>")

def company_requests(request):
    try:
        login_id = request.session.get('login_id')
        if not login_id:
            return redirect('company_home')
        
        company = tbl_company.objects.get(login_id=login_id)
        
        requests = tbl_requests.objects.filter(
            jobpost_id__company_id=company
        ).select_related(
            'jobpost_id',
            'batch_id',
            'course_id',
            'course_id__department_id'
        ).order_by('-request_date')
        
        for req in requests:
            assigned_students_count = tbl_student_schedule.objects.filter(
                request_id=req
            ).count()
            req.has_assigned_students = assigned_students_count > 0
            req.assigned_students_count = assigned_students_count
        
        pending_count = requests.filter(status='pending').count()
        bulk_pending_count = requests.filter(status='bulk_pending').count()
        approved_count = requests.filter(status='approved').count()
        rejected_count = requests.filter(status='rejected').count()
        
        assigned_count = 0
        for req in requests:
            if req.has_assigned_students or req.status == 'students_assigned':
                assigned_count += 1
        
        context = {
            'company': company,
            'requests': requests,
            'pending_count': pending_count,
            'bulk_pending_count': bulk_pending_count,
            'approved_count': approved_count,
            'rejected_count': rejected_count,
            'assigned_count': assigned_count,
            'total_requests': requests.count(),
        }
        
        return render(request, 'Company/view_requests.html', context)
    
    except Exception as e:
        return HttpResponse(f"<script>alert('Error: {str(e)}');window.location='/company_home/';</script>")

def view_request_details(request, request_id):
    try:
        login_id = request.session.get('login_id')
        if not login_id:
            return redirect('company_home')
        
        company = tbl_company.objects.get(login_id=login_id)
        req = get_object_or_404(tbl_requests, request_id=request_id, jobpost_id__company_id=company)
        
        jobpost = req.jobpost_id
        
        context = {
            'company': company,
            'request': req,
            'jobpost': jobpost,
        }
        
        return render(request, 'Company/request_details.html', context)
        
    except Exception as e:
        return HttpResponse(f"<script>alert('Error: {str(e)}');window.location='{reverse('company_requests')}';</script>")

view_requests = company_requests

def approve_request(request, request_id):
    try:
        login_id = request.session.get('login_id')
        if not login_id:
            return redirect('company_home')
        
        company = tbl_company.objects.get(login_id=login_id)
        req = tbl_requests.objects.get(request_id=request_id, jobpost_id__company_id=company)
        
        if request.method == "POST":
            req.status = 'approved'
            req.save()
            
            return HttpResponse(
                f"""
                <script>
                    alert('Request #{request_id} approved successfully!');
                    window.location='{reverse('company_requests')}';
                </script>
                """
            )
        
        context = {
            'request_id': request_id,
            'request': req,
        }
        return render(request, 'Company/approve_request.html', context)
        
    except tbl_requests.DoesNotExist:
        return HttpResponse(f"<script>alert('Request not found');window.location='{reverse('company_requests')}';</script>")
    except Exception as e:
        return HttpResponse(f"<script>alert('Error: {str(e)}');window.location='{reverse('company_requests')}';</script>")

def reject_request(request, request_id):
    try:
        login_id = request.session.get('login_id')
        if not login_id:
            return redirect('company_home')
        
        company = tbl_company.objects.get(login_id=login_id)
        req = tbl_requests.objects.get(request_id=request_id, jobpost_id__company_id=company)
        
        if request.method == "POST":
            reason = request.POST.get('reason', 'No reason provided')
            
            req.status = 'rejected'
            req.save()
            
            return HttpResponse(
                f"""
                <script>
                    alert('Request #{request_id} rejected.\\n\\nReason: {reason}');
                    window.location='{reverse('company_requests')}';
                </script>
                """
            )
        
        context = {
            'request_id': request_id,
        }
        return render(request, 'Company/reject_request.html', context)
        
    except tbl_requests.DoesNotExist:
        return HttpResponse(f"<script>alert('Request not found');window.location='{reverse('company_requests')}';</script>")
    except Exception as e:
        return HttpResponse(f"<script>alert('Error: {str(e)}');window.location='{reverse('company_requests')}';</script>")

def schedule_job(request, request_id):
    try:
        login_id = request.session.get('login_id')
        if not login_id:
            return redirect('company_home')
        
        company = tbl_company.objects.get(login_id=login_id)
        req = get_object_or_404(
            tbl_requests, 
            request_id=request_id, 
            jobpost_id__company_id=company
        )
        
        if request.method == "POST":
            stage = request.POST.get('stage')
            schedule_date = request.POST.get('schedule_date')
            selected_students = request.POST.getlist('selected_students[]')
            
            if not selected_students:
                return HttpResponse(
                    f"""
                    <script>
                        alert('Please select at least one student!');
                        window.location='{reverse('schedule_job', args=[request_id])}';
                    </script>
                    """
                )
            
            interview_schedule = tbl_interview_schedule.objects.create(
                schedule_date=schedule_date,
                stage=stage,
                status='scheduled',
                request_id=req
            )
            
            for student_id in selected_students:
                student = tbl_student.objects.get(student_id=student_id)
                student_schedule = tbl_student_schedule.objects.get(
                    student_id=student,
                    request_id=req,
                    status='assigned'
                )
                student_schedule.schedule_id = interview_schedule
                student_schedule.save()
            
            return HttpResponse(
                f"""
                <script>
                    alert('Students scheduled successfully!');
                    window.location='{reverse('view_request_details', args=[request_id])}';
                </script>
                """
            )
        
        details = tbl_interview_schedule.objects.filter(request_id_id=request_id)
        
        existing_stages = details.values_list('stage', flat=True)
        
        options = {
            'aptitude': 'Aptitude',
            'aptitude_technical': 'Aptitude & Technical',
            'interview': 'Interview',
            'technical_hr': 'Technical & HR',
            'hr': 'HR',
            'aptitude_technical_hr': 'Aptitude, Technical & HR',
            'completed': 'Completed'
        }
        
        assigned_student_schedules = tbl_student_schedule.objects.filter(
            request_id=req,
            status='assigned'
        ).select_related('student_id')
        
        scheduled_student_ids = []
        for detail in details:
            scheduled = tbl_student_schedule.objects.filter(
                schedule_id=detail
            ).values_list('student_id_id', flat=True)
            scheduled_student_ids.extend(scheduled)
        
        available_students = [schedule.student_id for schedule in assigned_student_schedules 
                              if schedule.student_id.student_id not in scheduled_student_ids]
        
        context = {
            'details': details,
            'options': options,
            'existing_stages': existing_stages,
            'requestid': request_id,
            'request': req,
            'company': company,
            'available_students': available_students,
            'total_assigned': len(assigned_student_schedules),
            'available_count': len(available_students),
            'scheduled_count': len(scheduled_student_ids),
        }
        
        return render(request, 'company/schedule_job.html', context)
        
    except Exception as e:
        return HttpResponse(f"<script>alert('Error: {str(e)}');window.location='{reverse('company_requests')}';</script>")