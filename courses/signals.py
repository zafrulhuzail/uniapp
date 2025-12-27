from django.db.models.signals import post_save
from django.dispatch import receiver
from courses.models import Section, Enrollment
from accounts.models import Student

@receiver(post_save, sender=Section)
def enroll_students_when_mandatory_section_created(sender, instance: Section, created: bool, **kwargs):
    if not created:
        return

    # only auto-enroll if it’s mandatory
    if not instance.is_mandatory:
        return

    students = Student.objects.filter(semester=instance.semester)

    Enrollment.objects.bulk_create(
        [Enrollment(student=st, section=instance) for st in students],
        ignore_conflicts=True
    )
