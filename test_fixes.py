#!/usr/bin/env python
"""
Test script to validate the fixes made to the placement system
Run with: python test_fixes.py
"""

import os
import sys
import django
from datetime import date, timedelta

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'catalystProject.settings')
django.setup()

from adminapp.models import tbl_requests, tbl_student_schedule, tbl_interview_schedule
from guestapp.models import tbl_company, tbl_student, tbl_login
from companyapp.models import tbl_jobpost
from catalystProject.constants import *

def test_status_constants():
    """Test that status constants are properly defined"""
    print("=== TESTING STATUS CONSTANTS ===")

    # Test all required statuses exist
    required_student_statuses = ['assigned', 'scheduled', 'interviewed', 'selected', 'rejected']
    for status in required_student_statuses:
        if status not in STUDENT_SCHEDULE_STATUS.values():
            print(f"❌ Missing student status: {status}")
            return False

    required_request_statuses = ['pending', 'bulk_pending', 'approved', 'rejected']
    for status in required_request_statuses:
        if status not in REQUEST_STATUS.values():
            print(f"❌ Missing request status: {status}")
            return False

    print("✅ All status constants properly defined")
    return True

def test_student_assignment_logic():
    """Test that student assignment logic works correctly"""
    print("\n=== TESTING STUDENT ASSIGNMENT LOGIC ===")

    try:
        # Get some test data
        assigned_students = tbl_student_schedule.objects.filter(status='assigned')
        scheduled_students = tbl_student_schedule.objects.filter(status='scheduled')
        rejected_students = tbl_student_schedule.objects.filter(status='rejected')

        print(f"Found {assigned_students.count()} assigned students")
        print(f"Found {scheduled_students.count()} scheduled students")
        print(f"Found {rejected_students.count()} rejected students")

        # Check that scheduled students have interview schedules
        scheduled_without_interview = scheduled_students.filter(schedule_id__isnull=True)
        if scheduled_without_interview.exists():
            print(f"❌ Found {scheduled_without_interview.count()} scheduled students without interview schedules")
            return False

        # Check that rejected students don't have future schedules
        rejected_with_future_schedule = rejected_students.filter(schedule_id__isnull=False)
        if rejected_with_future_schedule.exists():
            print(f"⚠️  Found {rejected_with_future_schedule.count()} rejected students with interview schedules (might be from previous rounds)")

        print("✅ Student assignment logic appears correct")
        return True

    except Exception as e:
        print(f"❌ Error testing student assignment logic: {e}")
        return False

def test_business_validation():
    """Test that business validation function exists and works"""
    print("\n=== TESTING BUSINESS VALIDATION ===")

    try:
        from adminapp.views import validate_request_creation
        print("✅ Business validation function exists")

        # Test with sample data if available
        try:
            # Look for non-expired job posts
            jobpost = tbl_jobpost.objects.filter(
                application_end_date__gte=date.today(),
                status='open'
            ).first()

            if jobpost:
                from adminapp.models import tbl_batch, tbl_course
                batch = tbl_batch.objects.first()
                course = tbl_course.objects.first()

                if batch and course:
                    # This should work without error
                    eligible_count = validate_request_creation(jobpost, batch, course, 1)
                    print(f"✅ Business validation works (found {eligible_count} eligible students)")
                else:
                    print("⚠️  Cannot test validation - missing batch/course data")
            else:
                print("⚠️  Cannot test validation - no active job posts found (all expired)")

        except Exception as e:
            print(f"❌ Business validation test failed: {e}")
            return False

        return True

    except ImportError:
        print("❌ Business validation function not found")
        return False

def test_database_consistency():
    """Test database consistency"""
    print("\n=== TESTING DATABASE CONSISTENCY ===")

    issues = []

    # Check for invalid status values in student schedules
    invalid_student_statuses = tbl_student_schedule.objects.exclude(
        status__in=STUDENT_SCHEDULE_STATUS.values()
    )

    if invalid_student_statuses.exists():
        issues.append(f"Found {invalid_student_statuses.count()} student schedules with invalid status values")

    # Check for invalid request statuses
    invalid_request_statuses = tbl_requests.objects.exclude(
        status__in=REQUEST_STATUS.values()
    )

    if invalid_request_statuses.exists():
        issues.append(f"Found {invalid_request_statuses.count()} requests with invalid status values")

    # Check for scheduled students without interview schedules
    scheduled_without_schedule = tbl_student_schedule.objects.filter(
        status='scheduled',
        schedule_id__isnull=True
    )

    if scheduled_without_schedule.exists():
        issues.append(f"Found {scheduled_without_schedule.count()} scheduled students without interview schedules")

    if issues:
        for issue in issues:
            print(f"❌ {issue}")
        return False
    else:
        print("✅ Database consistency checks passed")
        return True

def main():
    """Run all tests"""
    print("🔍 TESTING DJANGO PLACEMENT SYSTEM FIXES")
    print("=" * 50)

    tests = [
        test_status_constants,
        test_student_assignment_logic,
        test_business_validation,
        test_database_consistency,
    ]

    passed = 0
    total = len(tests)

    for test in tests:
        if test():
            passed += 1

    print("\n" + "=" * 50)
    print(f"📊 TEST RESULTS: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All fixes validated successfully!")
    else:
        print("⚠️  Some tests failed - review the output above")

    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)