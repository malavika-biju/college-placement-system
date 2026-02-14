from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from django.contrib import messages
from django.db.models import Q
from .models import tbl_jobpost              
from adminapp.models import tbl_requests, tbl_student_schedule, tbl_interview_schedule
from guestapp.models import tbl_company, tbl_student
from adminapp.email_utils import send_company_action_email_to_admin  # Added import
from django.core.mail import send_mail
from django.conf import settings

def send_interview_email_to_student(student, request, company, stage, schedule_date):
    """Send interview schedule email to student"""
    try:
        subject = f"Interview Scheduled: {company.company_name} - {request.jobpost_id.position}"
        
        message = f"""
        Dear {student.student_name},
        
        You have been scheduled for an interview with {company.company_name}.
        
        Interview Details:
        - Position: {request.jobpost_id.position}
        - Stage: {stage.replace('_', ' ').title()}
        - Date: {schedule_date}
        - Company: {company.company_name}
        
        Please be prepared and arrive on time.
        
        Best regards,
        Placement Cell
        """
        
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[student.email],
            fail_silently=True,
        )
        
        print(f"[EMAIL] Interview schedule sent to {student.email}")
        return True
        
    except Exception as e:
        print(f"[EMAIL ERROR] Failed to send to {student.email}: {str(e)}")
        return False

def send_placement_email_to_student(student, request, company):
    """Send placement congratulation email to student"""
    try:
        subject = f"🎉 Congratulations! Placement Offer - {company.company_name}"
        
        message = f"""
        Dear {student.student_name},
        
        CONGRATULATIONS!
        
        We are pleased to inform you that you have been SELECTED for the position of:
        
        {request.jobpost_id.position}
        at {company.company_name}
        
        You have successfully completed all interview stages and have been placed!
        
        The company will contact you shortly with further details regarding your joining process.
        
        This is a significant achievement. We wish you all the best for your career!
        
        Warm regards,
        Placement Cell
        """
        
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[student.email],
            fail_silently=True,
        )
        
        print(f"[EMAIL] Placement congratulation sent to {student.email}")
        return True
        
    except Exception as e:
        print(f"[EMAIL ERROR] Failed to send placement email: {str(e)}")
        return False

# Optional: Rejection email function
def send_rejection_email_to_student(student, request, company):
    """Send rejection email to student"""
    try:
        subject = f"Application Update: {company.company_name} - {request.jobpost_id.position}"
        
        message = f"""
        Dear {student.student_name},
        
        Thank you for your interest in the position of {request.jobpost_id.position} at {company.company_name}.
        
        After careful consideration, we regret to inform you that you have not been selected to proceed to the next stage of the interview process.
        
        We appreciate the time and effort you put into your application and encourage you to apply for future opportunities.
        
        We wish you the best in your job search.
        
        Sincerely,
        Placement Cell
        """
        
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[student.email],
            fail_silently=True,
        )
        
        print(f"[EMAIL] Rejection notification sent to {student.email}")
        return True
        
    except Exception as e:
        print(f"[EMAIL ERROR] Failed to send rejection email: {str(e)}")
        return False
    


def company_home(request):
    return render(request, 'company/index.html')

def company_profile(request):
    company = tbl_company.objects.get(login_id=request.session['login_id'])
    return render(request, 'company/profile.html', {'company': company})

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
        return HttpResponse("<script>alert('Job Posted Successfully');window.location='/companyapp/jobpost/';</script>")
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
        
        return render(request, 'company/view_requests.html', context)
    
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
        
        return render(request, 'company/request_details.html', context)
        
    except Exception as e:
        return HttpResponse(f"<script>alert('Error: {str(e)}');window.location='{reverse('company_requests')}';</script>")

view_requests = company_requests

def automate_student_selection(request, request_id):
    """Automated student selection based on scoring algorithm"""
    try:
        from .automation import StudentSelectionAutomation
        
        login_id = request.session.get('login_id')
        if not login_id:
            return redirect('company_home')
        
        company = tbl_company.objects.get(login_id=login_id)
        req = get_object_or_404(tbl_requests, request_id=request_id, jobpost_id__company_id=company)
        
        # Check if there are interviewed students
        interviewed_count = tbl_student_schedule.objects.filter(
            request_id=req,
            status='interviewed'
        ).count()
        
        if interviewed_count == 0:
            return HttpResponse(
                f"""
                <script>
                    alert('No interviewed students found for automation. Students must be interviewed first.');
                    window.location='{reverse('company_requests')}';
                </script>
                """
            )
        
        # Execute automation
        automation = StudentSelectionAutomation(request_id)
        result = automation.execute_automation()
        
        if result['success']:
            message = f"""
                Automation completed successfully!
                
                Total Students: {result['total_students']}
                Selected: {result['selected_count']}
                Rejected: {result['rejected_count']}
                Selection Rate: {result['selection_rate']}%
                Average Score: {result['avg_score']}
                Top Score: {result['top_score']}
                
                Students have been notified of their status.
            """
        else:
            # Removed email calls from here since they don't make sense in automation failure
            message = f"Automation failed: {result['message']}"
        
        return HttpResponse(
            f"""
            <script>
                alert('{message}');
                window.location='{reverse('company_requests')}';
            </script>
            """
        )
        
    except Exception as e:
        return HttpResponse(f"<script>alert('Error: {str(e)}');window.location='{reverse('company_requests')}';</script>")

def preview_automation_results(request, request_id):
    """Preview automation results without applying them"""
    try:
        from .automation import preview_automation
        
        login_id = request.session.get('login_id')
        if not login_id:
            return JsonResponse({'success': False, 'message': 'Not logged in'})
        
        company = tbl_company.objects.get(login_id=login_id)
        req = get_object_or_404(tbl_requests, request_id=request_id, jobpost_id__company_id=company)
        
        # Get preview
        result = preview_automation(request_id)
        
        return JsonResponse(result)
        
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})

def approve_request(request, request_id):
    try:
        login_id = request.session.get('login_id')
        if not login_id:
            return redirect('company_home')
        
        company = tbl_company.objects.get(login_id=login_id)
        req = get_object_or_404(tbl_requests, request_id=request_id, jobpost_id__company_id=company)
        
        if request.method == "POST":
            old_status = req.status 
            req.status = 'approved'
            req.save()
            send_company_action_email_to_admin(req, 'approved')
            return HttpResponse(
                f"""
                <script>
                    alert('Request #{request_id} approved successfully! Email notification sent to admin.');
                    window.location='{reverse('company_requests')}';
                </script>
                """
            )
        
        context = {
            'request_id': request_id,
            'request': req,
        }
        return render(request, 'company/approve_request.html', context)
        
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
            old_status = req.status
            
            req.status = 'rejected'
            req.save()

            send_company_action_email_to_admin(req, 'rejected')
            
            return HttpResponse(
                f"""
                <script>
                    alert('Request #{request_id} rejected.\\n\\nReason: {reason}\\n\\nEmail notification sent to admin.');
                    window.location='{reverse('company_requests')}';
                </script>
                """
            )
        
        context = {
            'request_id': request_id,
        }
        return render(request, 'company/reject_request.html', context)
        
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
                    "<script>alert('Please select at least one student');window.history.back();</script>"
                )

            if len(selected_students) > req.student_count:
                return HttpResponse(
                    f"<script>alert('You can select only {req.student_count} students');window.history.back();</script>"
                )

            interview_schedule, _ = tbl_interview_schedule.objects.get_or_create(
                request_id=req,
                stage=stage,
                defaults={
                    'schedule_date': schedule_date,
                    'status': 'scheduled'
                }
            )

            eligible_schedules = tbl_student_schedule.objects.filter(
                request_id=req
            ).exclude(status__in=['rejected', 'selected'])

            students_placed = []

            for sch in eligible_schedules:
                student = sch.student_id

                if str(student.student_id) in selected_students:
                    sch.schedule_id = interview_schedule

                    if stage == 'completed':
                        sch.status = 'selected'
                        sch.save()
                        students_placed.append(student.student_name)
                        send_placement_email_to_student(student, req, company)
                    else:
                        sch.status = 'interviewed'
                        sch.save()
                        send_interview_email_to_student(
                            student,
                            req,
                            company,
                            stage,
                            schedule_date
                        )
                else:
                    sch.status = 'rejected'
                    sch.save()
                    send_rejection_email_to_student(student, req, company)

            if stage == 'completed':
                req.status = 'students_assigned'
                req.save()

            if stage == 'completed' and students_placed:
                names = ", ".join(students_placed[:3])
                if len(students_placed) > 3:
                    names += f" and {len(students_placed) - 3} more"

                message = (
                    f"{len(students_placed)} student(s) PLACED!\\n\\n"
                    f"Students: {names}"
                )
            else:
                message = "Round completed successfully!"

            return HttpResponse(
                f"<script>alert('{message}');"
                f"window.location='{reverse('view_request_details', args=[request_id])}';</script>"
            )

        details = tbl_interview_schedule.objects.filter(request_id=req)
        existing_stages = details.values_list('stage', flat=True)

        options = {
    'aptitude': 'Aptitude',
    'technical': 'Technical',
    'interview': 'HR',
    'completed': 'Completed'
   }

        

        available_students = tbl_student_schedule.objects.filter(
            request_id=req
        ).exclude(status__in=['rejected', 'selected']).select_related('student_id')

        context = {
            'details': details,
            'options': options,
            'existing_stages': existing_stages,
            'requestid': request_id,
            'request': req,
            'company': company,
            'available_students': [s.student_id for s in available_students],
            'available_count': available_students.count(),
        }

        return render(request, 'company/schedule_job.html', context)

    except Exception as e:
        return HttpResponse(
            f"<script>alert('Error: {str(e)}');"
            f"window.location='{reverse('company_requests')}';</script>"
        )
