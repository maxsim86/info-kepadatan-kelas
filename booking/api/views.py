from os import times
from sqlite3 import Timestamp
from rest_framework.decorators import api_view
from rest_framework.response import Response
from booking.models import Room, Booking, User, TimeSlot
from .serializer import (
    RoomSerializer,
    TimeSlotSerializer,
    UserSerializer,
    BookingSerializer,
)


@api_view(["GET"])
def getRoutes(request):
    routes = [
        "GET /api",
        "GET /api/users",
        "GET /api/rooms",
        "GET /api/rooms/:id",
        "GET /api/timeslots",
        "GET /api/timeslots/:id",
        "GET /api/bookings/ ",
        "GET /api/bookings/:id",
    ]
    return Response(routes)

    # user model

def getUser(request):
    user = User.objects.get.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

def getUser(request, pk):
    user = User.objects.get(id=pk)
    serializer = UserSerializer(user, many=False)

    # Room Model
def getRoom(request):
    rooms = Room.objects.get(id=pk)
    serializer = RoomSerializer(rooms, many=False)
    return Response(serializer.data)

def getRoom(request, pk):
    rooms = Room.objects.get(id=pk)
    serializer = TimeSlotSerializer(rooms, many=False)
    return Response(serializer.data)

#timeslot model
def getTimeSlots(request):
    timeslots = TimeSlot.objects.all()
    serializer = TimeSlotSerializer(timeslots, many=True)

def getTimeSlot(request, pk):
    timeslot = TimeSlot
    serializer = TimeSlotSerializer(TimeSlot, many=False)
    return Response(serializer.data)

#booking model

def getBooking(request):
    bookings = Booking.objects.all()
    serializer = BookingSerializer(bookings, many=True)
    return Response(serializer.data)

def getBooking(request, pk):
    booking = Booking.objects.get(id=pk)
    serializer = BookingSerializer(booking, many=False)
    return Response(serializer.data)
    
    