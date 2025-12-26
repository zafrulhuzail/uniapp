from dataclasses import dataclass
from datetime import time
from typing import List, Optional

from courses.models import SectionMeeting, Enrollment
from timetable.models import StudentPersonalEvent

@dataclass
class TimeTableItem:
    type: str  # 'course' or 'personal_event'
    title: str
    weekday: int
    start_time: time
    end_time: time
    building: str
    room: str
    description: Optional[str] = None

def get_student_timetable(student_id: int) -> List[TimeTableItem]:
    #course meetings via enrollments
    meetings = SectionMeeting.objects.filter(
        section__enrollment__student__id=student_id
    ).select_related('section__course', 'building', 'room')

    courses_items = [ 
        TimeTableItem(
            type='course',
            title=meeting.section.course.title,
            weekday=meeting.weekday,
            start_time=meeting.start_time,
            end_time=meeting.end_time,
            building=meeting.building.name,
            room=meeting.room.name
        )
        for meeting in meetings
    ]

    personal = StudentPersonalEvent.objects.filter(student__student_id=student_id)\
        .select_related("building", "room")
    
    personal_items = [
        TimeTableItem(
            type='personal_event',
            title=event.title,
            weekday=event.weekday,
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