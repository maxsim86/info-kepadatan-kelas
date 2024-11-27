from django.db import models
from appointment.models import Appointment
from django.contrib.auth.models import User

#Create your models here.

class Room(models.Model):
     name = models.CharField(max_length=100)
     description = models.TextField()
     capacity = models.PositiveIntegerField()
     available = models.BooleanField(default=True)

     def __str__(self):
         return self.name
    
class Booking(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
         return f"{self.user.username} - {self.room.name} ({'self.date'})"


class RoomBookingSlot(AppointmentSlot):
    room = models.ForeignKey('booking.Room', on_delete=models.CASCADE, related_name='booking_slots')
    
    def __str__(self):
        return f"{self.room.name}-{self.start_time} to {self.end_time}"