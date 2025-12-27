from django.shortcuts import render
from django.http import HttpResponse
from .services import get_student_timetable
from django.contrib.auth.decorators import login_required
from datetime import datetime
# Create your views here.

WEEKDAY_NAMES = {
    0: "Monday",
    1: "Tuesday",
    2: "Wednesday",
    3: "Thursday",
    4: "Friday",
    5: "Saturday",
    6: "Sunday"
}


def student_timetable(request, student_id):
  items = get_student_timetable(student_id)
  return render(request, 'timetable/student_timetable.html', {
        student_id: student_id,
        'items': items,
    })

@login_required
def my_timetable(request):
    user = request.user

    if not hasattr(user, 'student'):
        return HttpResponse("You are not a student.", status=403)

    student = user.student
    items = get_student_timetable(student.student_id)

    return render(request, 'timetable/student_timetable.html', {
        'student_first_name': student.first_name,
        'student_last_name': student.last_name,
        'items': items,
    })

@login_required
def day_view(request):
    user = request.user
    current_day = datetime.now().weekday()

    if not hasattr(user, 'student'): 
        return HttpResponse("You are not a student.", status=403)
    
    student = user.student
    items = get_student_timetable(student.student_id)

    day_items = []
    for item in items:
        if item.weekday == WEEKDAY_NAMES[current_day]:
            day_items.append(item)

    return render(request, 'timetable/student_timetable.html', {
        'student_first_name': student.first_name,
        'student_last_name': student.last_name,
        'items': day_items,
    })