from django.db import models

# Create your models here.
class Building(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Room(models.Model):
    name = models.CharField(max_length=100, unique=True)
    building = models.ForeignKey(Building, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class RoomOccupancy(models.Model):
    building = models.ForeignKey(Building, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return f"{self.room.name} in {self.building.name} from {self.start_time} to {self.end_time}"
