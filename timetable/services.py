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
    is_mandatory: Optional[bool] = None
    section_id: Optional[int] = None
    event_id: Optional[int] = None
    building_id: Optional[int] = None
    room_id: Optional[int] = None

def get_student_timetable(student_id: int) -> List[TimeTableItem]:
    student = Student.objects.get(student_id=student_id)

    meetings = (
        SectionMeeting.objects.filter(
            section__enrollment__student=student,
            section__enrollment__show_on_timetable=True,
        )
        .select_related("section__course", "building", "room")
        .distinct()
    )

    course_items: List[TimeTableItem] = []
    for m in meetings:
        course_items.append(
            TimeTableItem(
                type="course",
                title=m.section.course.title,
                weekday=m.weekday,
                start_time=m.start_time,
                end_time=m.end_time,
                building=m.building.name if m.building else "",
                room=m.room.name if m.room else "",
                description="",
                section_id=m.section_id,
            )
        )

    personal_qs = (
        StudentPersonalEvent.objects.filter(student=student)
        .select_related("building", "room")
    )

    personal_items: List[TimeTableItem] = []
    for ev in personal_qs:
        personal_items.append(
            TimeTableItem(
                type="personal_event",
                title=ev.title,
                weekday=ev.weekday,
                start_time=ev.start_time,
                end_time=ev.end_time,
                building=ev.building.name if ev.building else "",
                room=ev.room.name if ev.room else "",
                description=ev.description or "",
                event_id=ev.id,
                building_id=ev.building_id,
                room_id=ev.room_id,
            )
        )

    items = course_items + personal_items
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