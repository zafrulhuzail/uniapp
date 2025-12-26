from django.db import models
from accounts.models import Semester, Professor, Student
from buildings.models import Building, Room

# Create your models here.
class Course(models.Model):
    title = models.CharField(max_length=200)
    
    def __str__(self):
        return self.title


class Section(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('course', 'semester', 'professor')

    def __str__(self):
        return f"{self.course.title} - {self.semester.name} - {self.professor.user.first_name} {self.professor.user.last_name}"

class Weekday(models.IntegerChoices):
        MONDAY = 1, "Monday"
        TUESDAY = 2, "Tuesday"
        WEDNESDAY = 3, "Wednesday"
        THURSDAY = 4, "Thursday"
        FRIDAY = 5, "Friday"
        SATURDAY = 6, "Saturday"
        SUN = 7, "Sunday"

class SectionMeeting(models.Model):

    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    weekday = models.IntegerField(choices=Weekday.choices, default=Weekday.MONDAY)
    start_time = models.TimeField()
    end_time = models.TimeField()
    building = models.ForeignKey(Building, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.section} meets on {self.weekday} from {self.start_time} to {self.end_time} at {self.room}"

class Enrollment(models.Model):
    student = models.ForeignKey('accounts.Student', on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('student', 'section')

    def __str__(self):
        return f"{self.student} enrolled in {self.section}"
    