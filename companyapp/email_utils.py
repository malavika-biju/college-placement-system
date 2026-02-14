# companyapp/email_utils.py
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from .models import tbl_jobpost
from guestapp.models import tbl_company
import datetime

def send_interview_schedule_email_to_students(schedule, student_emails):
    """
    Send interview schedule emails to students using HTML template
    """
    try:
        request = schedule.request_id
        company = request.jobpost_id.company_id
        jobpost = request.jobpost_id
        
        subject = f"📅 Interview Scheduled: {company.company_name} - {jobpost.position}"
        
        # Prepare context for HTML template
        context = {
            'company': company,
            'jobpost': jobpost,
            'schedule': schedule,
            'request': request,
            'site_url': 'http://localhost:8000',
        }
        
        # Render HTML template
        html_content = render_to_string('company/emails/interview_schedule.html', context)
        text_content = strip_tags(html_content)
        
        # Send to each student
        success_count = 0
        for email in student_emails:
            try:
                email_msg = EmailMultiAlternatives(
                    subject=subject,
                    body=text_content,
                    from_email=settings.EMAIL_HOST_USER,
                    to=[email],
                )
                email_msg.attach_alternative(html_content, "text/html")
                email_msg.send(fail_silently=True)
                success_count += 1
            except Exception as e:
                print(f"[STUDENT EMAIL ERROR] Failed to send to {email}: {str(e)}")
        
        print(f"[INTERVIEW EMAILS] Sent HTML email to {success_count}/{len(student_emails)} students")
        return success_count > 0
        
    except Exception as e:
        print(f"[INTERVIEW EMAIL ERROR] {str(e)}")
        return False

def send_deadline_reminder_to_company(jobpost):
    """
    Send deadline reminder using HTML template
    """
    try:
        company = jobpost.company_id
        days_left = (jobpost.application_end_date - datetime.date.today()).days
        
        subject = f"⏰ Deadline Reminder: {jobpost.position} - {days_left} days left"
        
        # Prepare context
        context = {
            'company': company,
            'jobpost': jobpost,
            'days_remaining': days_left,
            'deadline_date': jobpost.application_end_date,
            'site_url': 'http://localhost:8000',
        }
        
        # Render HTML template
        html_content = render_to_string('company/emails/deadline_reminder.html', context)
        text_content = strip_tags(html_content)
        
        # Create email
        email_msg = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=settings.EMAIL_HOST_USER,
            to=[company.contact_email],
        )
        email_msg.attach_alternative(html_content, "text/html")
        email_msg.send(fail_silently=True)
        
        print(f"[DEADLINE REMINDER] Sent HTML email for job #{jobpost.jobpost_id}")
        return True
        
    except Exception as e:
        print(f"[DEADLINE REMINDER ERROR] {str(e)}")
        return False

def check_and_send_deadline_reminders():
    """
    Check all jobs and send deadline reminders
    Call this daily from a cron job or admin dashboard
    """
    try:
        today = datetime.date.today()
        jobs = tbl_jobpost.objects.filter(
            status='open',
            application_end_date__gte=today
        )
        
        reminder_count = 0
        for job in jobs:
            days_left = (job.application_end_date - today).days
            # Send reminders 7, 3, and 1 days before deadline
            if days_left in [7, 3, 1]:
                if send_deadline_reminder_to_company(job):
                    reminder_count += 1
        
        print(f"[DEADLINE CHECK] Sent {reminder_count} reminders")
        return reminder_count
        
    except Exception as e:
        print(f"[DEADLINE CHECK ERROR] {str(e)}")
        return 0