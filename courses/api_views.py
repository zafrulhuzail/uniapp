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