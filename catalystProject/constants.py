# Status constants to ensure consistency across the application

# Login/Registration Status
LOGIN_STATUS = {
    'REQUESTED': 'requested',
    'CONFIRMED': 'confirmed',
    'REJECTED': 'rejected',
}

# Request Status (from admin to company)
REQUEST_STATUS = {
    'PENDING': 'pending',
    'BULK_PENDING': 'bulk_pending',
    'APPROVED': 'approved',
    'REJECTED': 'rejected',
    'STUDENTS_ASSIGNED': 'students_assigned',  # Legacy, consider removing
}

# Student Schedule Status (student placement status)
STUDENT_SCHEDULE_STATUS = {
    'ASSIGNED': 'assigned',      # Assigned to company, eligible for interviews
    'SCHEDULED': 'scheduled',    # Assigned to specific interview round
    'INTERVIEWED': 'interviewed', # Completed interview
    'SELECTED': 'selected',      # Selected by company
    'REJECTED': 'rejected',      # Rejected by company or failed interview
}

# Job Post Status
JOB_POST_STATUS = {
    'OPEN': 'open',
    'CLOSED': 'closed',
    'EXPIRED': 'expired',
}

# Interview Schedule Status
INTERVIEW_SCHEDULE_STATUS = {
    'SCHEDULED': 'scheduled',
    'COMPLETED': 'completed',
    'CANCELLED': 'cancelled',
}