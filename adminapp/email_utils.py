# adminapp/email_utils.py
from django.core.mail import send_mail
from django.conf import settings

def send_company_action_email_to_admin(request, action):
    """
    Send email to admin when company approves/rejects a request
    action = 'approved' or 'rejected'
    """
    try:
        company = request.jobpost_id.company_id
        jobpost = request.jobpost_id
        
        # Email subject
        if action == 'approved':
            subject = f"✅ Company Approved Request #{request.request_id}"
            status_color = "GREEN"
        else:
            subject = f"❌ Company Rejected Request #{request.request_id}"
            status_color = "RED"
        
        # Email content
        message = f"""
        COMPANY ACTION NOTIFICATION
        
        Company: {company.company_name}
        Email: {company.contact_email}
        Phone: {company.contact_number}
        
        Request ID: #{request.request_id}
        Action: {action.upper()}
        
        Job Details:
        - Position: {jobpost.position}
        - Cutoff Mark: {jobpost.cutoff_mark}%
        - Deadline: {jobpost.application_end_date}
        
        Student Details:
        - Batch: {request.batch_id.batch_year}
        - Course: {request.course_id.course_name}
        - Department: {request.course_id.department_id.department_name}
        - Number of Students: {request.student_count}
        
        Action Date: {request.request_date}
        
        Please check the admin dashboard for more details.
        
        ---
        Catalyst Placement System
        Automated Notification
        """
        
        # Send to admin email (YOUR EMAIL)
        admin_email = 'malumr2006@gmail.com'  # ← This is YOUR email from settings
        
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,  # malumr2006@gmail.com
            recipient_list=[admin_email],
            fail_silently=True,  # Don't crash if email fails
        )
        
        print(f"[EMAIL SENT] Company {action} request #{request.request_id} → {admin_email}")
        return True
        
    except Exception as e:
        print(f"[EMAIL ERROR] {str(e)}")
        return False