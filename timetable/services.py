from dataclasses import dataclass
from datetime import time
from typing import List, Optional

from courses.models import SectionMeeting, Enrollment
from timetable.models import StudentPersonalEvent
from accounts.models import Student

@dataclass
class TimeTableItem:
    type: str  # 'course' or 'personal_event'
    title: str
    weekday: str
    start_time: time
    end_time: time
    building: str
    room: str
    description: Optional[str] = None

def get_student_timetable(student_id: int) -> List[TimeTableItem]:
    # student_id here means Student.student_id
    student = Student.objects.get(student_id=student_id)

    # 1) get enrollments for this student
    enrollments = Enrollment.objects.filter(student=student)

    # 2) get the sections from those enrollments
    sections = [e.section for e in enrollments]

    # 3) get meetings for those sections
    meetings = SectionMeeting.objects.filter(section__in=sections)

    courses_items = [
        TimeTableItem(
            type="course",
            title=m.section.course.title,
            weekday=m.get_weekday_display(),
            start_time=m.start_time,
            end_time=m.end_time,
            building=m.building.name,
            room=m.room.name,
        )
        for m in meetings
    ]

    personal = StudentPersonalEvent.objects.filter(student__student_id=student_id)\
        .select_related("building", "room")
    
    personal_items = [
        TimeTableItem(
            type='personal_event',
            title=event.title,
            weekday=event.get_weekday_display(),
            start_time=event.start_time,
            end_time=event.end_time,
            building=event.building.name,
            room=event.room.name,
            description=event.description
        )
        for event in personal
    ]

    items = courses_items + personal_items
    items.sort(key=lambda x: (x.weekday, x.start_time))
    return items

def get_student_timetable_specific_course_type(student_id: int, is_mandatory: bool = True) -> List[TimeTableItem]:
    # student_id here means Student.student_id
    student = Student.objects.get(student_id=student_id)

    # 1) get enrollments for this student
    enrollments = Enrollment.objects.filter(student=student)

    # 2) get the sections from those enrollments
    sections = [e.section for e in enrollments if e.section.is_mandatory == is_mandatory]

    # 3) get meetings for those sections
    meetings = SectionMeeting.objects.filter(section__in=sections)

    courses_items = [
        TimeTableItem(
            type="course",
            title=m.section.course.title,
            weekday=m.get_weekday_display(),
            start_time=m.start_time,
            end_time=m.end_time,
            building=m.building.name,
            room=m.room.name,
        )
        for m in meetings
    ]

    items = courses_items
    items.sort(key=lambda x: (x.weekday, x.start_time))
    return items