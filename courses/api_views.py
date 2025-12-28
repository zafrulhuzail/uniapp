from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Section, Student, Enrollment, Course
from .services import *

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_mandatory_courses(request):

    is_mandatory = True

    mandatory_courses = get_student_courses(request.user, is_mandatory)

    return Response({"mandatory_courses": mandatory_courses})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_elective_courses(request):
    
    is_mandatory = False

    elective_courses = get_student_courses(request.user, is_mandatory)

    return Response({"elective_courses": elective_courses})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_get_enrolled_courses(request):
    user = request.user

    if not hasattr(user, 'student'):
        return Response({"detail": "You are not a student."}, status=403)

    student = user.student
    enrollments = Enrollment.objects.filter(student=student)

    data = [
        {
            "course_title": enrollment.section.course.title,
            "section_id": enrollment.section.id,
            "show_on_timetable": enrollment.show_on_timetable,
        }
        for enrollment in enrollments
    ]

    return Response({
        "student_first_name": student.first_name,
        "student_last_name": student.last_name,
        "enrollments": data,
    })