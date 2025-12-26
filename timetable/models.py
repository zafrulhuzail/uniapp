from django.db import models
from accounts.models import Student
from buildings.models import Building, Room
from courses.models import Weekday
# Create your models here.

class StudentPersonalEvent(models.Model):
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    weekday = models.IntegerField(choices=Weekday.choices, default=Weekday.MONDAY)
    start_time = models.TimeField()
    end_time = models.TimeField()
    building = models.ForeignKey(Building, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.title} for {self.student.user.username} on {self.get_weekday_display()} from {self.start_time} to {self.end_time} at {self.room}"
    
