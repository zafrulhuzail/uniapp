from dataclasses import dataclass
from datetime import time
from typing import List, Optional
from django.db.models import Q

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

def _overlap_q(start: time, end: time) -> Q:
    # overlap: start < existing_end AND end > existing_start
    return Q(start_time__lt=end) & Q(end_time__gt=start)

def detect_conflict(
    *,
    student: Student,
    weekday: int,
    start_time: time,
    end_time: time,
    ignore_personal_event_id: Optional[int] = None,
    ignore_enrollment_id: Optional[int] = None,
) -> Optional[str]:
    """
    Returns a human-readable conflict message if conflict exists, else None.
    Conflicts against:
      - Personal events
      - Courses currently shown on timetable (Enrollment.show_on_timetable=True)
    """
    if end_time <= start_time:
        return "End time must be after start time."

    # 1) Personal events
    pe_qs = StudentPersonalEvent.objects.filter(
        student=student,
        weekday=weekday,
    ).filter(_overlap_q(start_time, end_time))

    if ignore_personal_event_id:
        pe_qs = pe_qs.exclude(id=ignore_personal_event_id)

    pe = pe_qs.first()
    if pe:
        return (
            f"Conflicts with personal event: {pe.title} "
            f"({pe.start_time.strftime('%H:%M')}–{pe.end_time.strftime('%H:%M')})."
        )

    # 2) Course meetings from currently visible enrollments
    enroll_qs = Enrollment.objects.filter(student=student, show_on_timetable=True)
    if ignore_enrollment_id:
        enroll_qs = enroll_qs.exclude(id=ignore_enrollment_id)

    cm_qs = (
        SectionMeeting.objects.filter(
            section__enrollment__in=enroll_qs,
            weekday=weekday,
        )
        .filter(_overlap_q(start_time, end_time))
        .select_related("section__course")
    )

    cm = cm_qs.first()
    if cm:
        title = cm.section.course.title
        return (
            f"Conflicts with course: {title} "
            f"({cm.start_time.strftime('%H:%M')}–{cm.end_time.strftime('%H:%M')})."
        )

    return None


def detect_conflict_for_section(
    *,
    student: Student,
    section_id: int,
    ignore_enrollment_id: Optional[int] = None,
) -> Optional[str]:
    """
    A section can have multiple meetings. If ANY meeting conflicts, return message.
    """
    meetings = SectionMeeting.objects.filter(section_id=section_id).only(
        "weekday", "start_time", "end_time"
    )

    for m in meetings:
        msg = detect_conflict(
            student=student,
            weekday=m.weekday,
            start_time=m.start_time,
            end_time=m.end_time,
            ignore_enrollment_id=ignore_enrollment_id,
        )
        if msg:
            return msg

    return None

def get_student_timetable(student_id: int) -> List[TimeTableItem]:
    # get current logged in student
    student = Student.objects.get(student_id=student_id)

    # from section meetings, filter those that enrolled by this student and show_on_timetable is True
    # then, fetch related objects: course, building, room
    # finally, distinct to avoid duplicates 
    meetings = (    
        SectionMeeting.objects.filter(
            section__enrollment__student=student,
            section__enrollment__show_on_timetable=True,
        )
        .select_related("section__course", "building", "room")
        .distinct()
    )

    # standardize to TimeTableItem
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
                description=m.description or "",
                section_id=m.section_id,
            )
        )

    # from student personal events, filter those that belong to this student
    # fetch related building and room object, instead of ids
    personal_qs = (
        StudentPersonalEvent.objects.filter(student=student)
        .select_related("building", "room")
    )

    # standardize to TimeTableItem
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

    # combine both course items and personal event items
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