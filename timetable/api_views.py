from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from datetime import datetime

from .views import WEEKDAY_NAMES
from .services import *
from courses.models import Enrollment


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_my_timetable(request):
    user = request.user

    if not hasattr(user, 'student'):
        return Response({"detail": "You are not a student."}, status=403)

    student = user.student
    items = get_student_timetable(student.student_id)

    data = [
        {
            "type": item.type,
            "title": item.title,
            "weekday": item.weekday,
            "start_time": item.start_time.strftime("%H:%M"),
            "end_time": item.end_time.strftime("%H:%M"),
            "building": item.building,
            "room": item.room,
            "description": item.description,
        }
        for item in items
    ]

    return Response({
        "student_first_name": student.first_name,
        "student_last_name": student.last_name,
        "items": data,
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_day_view(request):
    user = request.user
    current_day = datetime.now().weekday()

    if not hasattr(user, 'student'):
        return Response({"detail": "You are not a student."}, status=403)

    student = user.student
    items = get_student_timetable(student.student_id)

    day_items = []
    for item in items:
        if item.weekday == WEEKDAY_NAMES[current_day]:
            day_items.append(item)

    data = [
        {
            "type": item.type,
            "title": item.title,
            "weekday": item.weekday,
            "start_time": item.start_time.strftime("%H:%M"),
            "end_time": item.end_time.strftime("%H:%M"),
            "building": item.building,
            "room": item.room,
            "description": item.description,
        }
        for item in day_items
    ]

    return Response({
        "student_first_name": student.first_name,
        "student_last_name": student.last_name,
        "items": data,
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_my_timetable_mandatory_course(request):
    is_mandatory = True
    user = request.user

    if not hasattr(user, 'student'):
        return Response({"detail": "You are not a student."}, status=403)

    student = user.student
    items = get_student_timetable_specific_course_type(student.student_id, is_mandatory)

    data = [
        {
            "type": item.type,
            "title": item.title,
            "weekday": item.weekday,
            "start_time": item.start_time.strftime("%H:%M"),
            "end_time": item.end_time.strftime("%H:%M"),
            "building": item.building,
            "room": item.room,
            "description": item.description,
        }
        for item in items
    ]

    return Response({
        "student_first_name": student.first_name,
        "student_last_name": student.last_name,
        "items": data,
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_my_timetable_elective_course(request):
    is_mandatory = False
    user = request.user

    if not hasattr(user, 'student'):
        return Response({"detail": "You are not a student."}, status=403)

    student = user.student
    items = get_student_timetable_specific_course_type(student.student_id, is_mandatory)

    data = [
        {
            "type": item.type,
            "title": item.title,
            "weekday": item.weekday,
            "start_time": item.start_time.strftime("%H:%M"),
            "end_time": item.end_time.strftime("%H:%M"),
            "building": item.building,
            "room": item.room,
            "description": item.description,
        }
        for item in items
    ]

    return Response({
        "student_first_name": student.first_name,
        "student_last_name": student.last_name,
        "items": data,
    })

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def api_activate_show_on_timetable(request, enrollment_id):
    user = request.user

    if not hasattr(user, 'student'):
        return Response({"detail": "You are not a student."}, status=403)

    try:
        enrollment = Enrollment.objects.get(id=enrollment_id)
    except Enrollment.DoesNotExist:
        return Response({"detail": "Enrollment not found."}, status=404)

    # enrollment = Enrollment.objects.get(id=enrollment_id)

    enrollment.show_on_timetable = True
    enrollment.save()

    return Response({"detail": "Enrolled course activated to show on timetable."})