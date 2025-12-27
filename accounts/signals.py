from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import Student
from courses.models import Section, Enrollment

@receiver(post_save, sender=Student)
def enroll_new_student_in_mandatory_sections(sender, instance: Student, created: bool, **kwargs):
    if not created:
        return

    mandatory_sections = Section.objects.filter(
        semester=instance.semester,
        is_mandatory=True,
    )

    Enrollment.objects.bulk_create(
        [Enrollment(student=instance, section=s) for s in mandatory_sections],
        ignore_conflicts=True
    )
