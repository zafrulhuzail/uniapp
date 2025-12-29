from django.shortcuts import render
from django.http import HttpResponse

from buildings.models import Building, Room
from .services import get_student_timetable
from django.contrib.auth.decorators import login_required
from datetime import datetime, time
from courses.models import Enrollment
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

DAY_LABELS = [
    (1, "Monday"),
    (2, "Tuesday"),
    (3, "Wednesday"),
    (4, "Thursday"),
    (5, "Friday"),
    (6, "Saturday"),
    (7, "Sunday"),
]

def _minutes_since(day_start: time, t: time) -> int:
    return (t.hour * 60 + t.minute) - (day_start.hour * 60 + day_start.minute)

def student_timetable(request, student_id):
  items = get_student_timetable(student_id)
  return render(request, 'timetable/student_timetable.html', {
        student_id: student_id,
        'items': items,
    })

@login_required
def my_timetable(request):
    # get current logged in user and check if is student
    user = request.user
    if not hasattr(user, "student"):
        return HttpResponse("You are not a student.", status=403)

    # get student object
    student = user.student

    # filter enrollments for this student
    # fetch related section and course objects
    # up to here which courses enrolled by this student are known
    enrollments = (
        Enrollment.objects.filter(student=student)
        .select_related("section__course")
    )

    # prepare pool items for courses not shown on timetable
    # Column 1 | Column 2 | Column 3
    # Enrollment ID | Course Title | Section ID
    pool_items = [
        {"enrollment_id": e.id, "title": e.section.course.title, "section_id": e.section_id}
        for e in enrollments.filter(show_on_timetable=False)
    ]

    # create a set of dict
    # map section_id to enrollment_id for quick lookup later
    section_to_enrollment_id = {e.section_id: e.id for e in enrollments}

    # get timetable items for this student
    # all enrolled courses and personal events
    items = get_student_timetable(student.student_id)

    day_start = time(8, 0) # timetable starts at 08:00
    day_end = time(19, 25) # timetable ends at 19:25
    px_per_min = 5.0       # 2 pixels per minute

    total_minutes = _minutes_since(day_start, day_end) # 685 minutes
    grid_height = total_minutes * px_per_min # grid_height = 685 × 2.0 = 1370.0 pixels

    time_labels = [
        ("08:00", "08:45"), ("08:45", "09:30"),
        ("09:50", "10:35"), ("10:35", "11:20"),
        ("11:40", "12:25"), ("12:25", "13:10"),
        ("14:00", "14:45"), ("14:45", "15:30"),
        ("15:40", "16:25"), ("16:25", "17:10"),
        ("17:10", "17:55"), ("17:55", "18:40"),
        ("18:40", "19:25"),
    ]

    # compute pixels for time labels on the left side of timetable
    label_blocks = []
    for s, e in time_labels:
        sh, sm = map(int, s.split(":")) # "08:00".split(":") -> ["08", "00"] -> sh=8, sm=0
        eh, em = map(int, e.split(":")) # "08:45".split(":") -> ["08", "45"] -> eh=8, em=45

        # calculate top and height in pixels for frontend rendering
        top = _minutes_since(day_start, time(sh, sm)) * px_per_min  
        height = (_minutes_since(day_start, time(eh, em)) - _minutes_since(day_start, time(sh, sm))) * px_per_min

        # append to label_blocks list
        label_blocks.append({"text": f"{s} - {e}", "top": top, "height": height}) #need to change

    # compute pixels for each timetable item
    MIN_CARD_HEIGHT_PX = 70
    blocks = []

    for item in items:
        # validate weekday, skip if invalid
        if not isinstance(item.weekday, int) or item.weekday < 1 or item.weekday > 7:
            continue 

        start_minutes = _minutes_since(day_start, item.start_time) # 08:00 -> 0 minutes
        end_minutes = _minutes_since(day_start, item.end_time) # e.g., 09:30 -> 90 minutes

        start_minutes = max(0, start_minutes) # if class starts before day_start (8:00), set to 0
        end_minutes = min(total_minutes, end_minutes) # avoid overflow outside timetable grid
        if end_minutes <= start_minutes: # invalid time range, skip
            continue

        top = start_minutes * px_per_min
        height = max((end_minutes - start_minutes) * px_per_min, MIN_CARD_HEIGHT_PX) # ensure minimum height, e.g., 30 minutes class shows at least 70px

        enrollment_id = None
        if item.type == "course" and item.section_id is not None:
            enrollment_id = section_to_enrollment_id.get(item.section_id) #return enrollment id

        blocks.append({
            "type": item.type,
            "title": item.title,
            "weekday": item.weekday,
            "start_time": item.start_time.strftime("%H:%M"),
            "end_time": item.end_time.strftime("%H:%M"),
            "building": item.building,
            "room": item.room,
            "description": item.description or "",
            "top": top,
            "height": height,
            "color": "bg-pink-600" if item.type == "course" else "bg-orange-500",

            # courses
            "enrollment_id": enrollment_id,

            # personal events
            "event_id": getattr(item, "event_id", None),
            "building_id": getattr(item, "building_id", None),
            "room_id": getattr(item, "room_id", None),
        })

    buildings = Building.objects.all().order_by("name")
    rooms = Room.objects.all().order_by("name")

    return render(request, "timetable/my_timetable.html", {
        "student": student,
        "day_labels": DAY_LABELS,
        "blocks": blocks,
        "label_blocks": label_blocks,
        "grid_height": grid_height,
        "pool_items": pool_items,
        "buildings": buildings,
        "rooms": rooms,
    })

@login_required
def list_course_timetable(request):
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