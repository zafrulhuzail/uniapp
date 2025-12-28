from courses.models import Course, Section, Enrollment
from accounts.models import Student


def get_student_courses(user, is_mandatory=True)-> list:

    student = Student.objects.get(student_id=user.student.student_id)

    if not hasattr(user, 'student'):
        return Response({"error": "You are not a student."}, status=403)

    enrollments = Enrollment.objects.filter(student=student)

    sections = [e.section for e in enrollments]

    courses_id = Section.objects.filter(id__in=[s.id for s in sections if s.is_mandatory == is_mandatory])

    courses = Course.objects.filter(id__in=[s.course.id for s in courses_id])

    filtered_courses = [
        {
            "title": course.title,
        }
        for course in courses
    ]

    return filtered_courses