from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Semester(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_id = models.BigIntegerField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    semester = models.ForeignKey(Semester, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.student_id})"
    

class Professor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    employee_id = models.BigIntegerField(unique=True)