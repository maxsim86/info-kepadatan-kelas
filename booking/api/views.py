from os import times
#from sqlite3 import TimeStamp
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
@api_view(['GET'])
def getUsers(request):
    users = User.objects.get.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getUser(request, pk):
    user = User.objects.get(id=pk)
    serializer = UserSerializer(user, many=False)

    # Room Model
@api_view(['GET'])
def getRooms(request):
    rooms = Room.objects.get(id=pk)
    serializer = RoomSerializer(rooms, many=False)
    return Response(serializer.data)
@api_view(['GET'])
def getRoom(request, pk):
    rooms = Room.objects.get(id=pk)
    serializer = TimeSlotSerializer(rooms, many=False)
    return Response(serializer.data)

#timeslot model
@api_view(['GET'])
def getTimeSlots(request):
    timeslots = TimeSlot.objects.all()
    serializer = TimeSlotSerializer(timeslots, many=True)
@api_view(['GET'])
def getTimeSlot(request, pk):
    timeslot = TimeSlot
    serializer = TimeSlotSerializer(TimeSlot, many=False)
    return Response(serializer.data)

#booking model
@api_view(['GET'])
def getBookings(request):
    bookings = Booking.objects.all()
    serializer = BookingSerializer(bookings, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getBooking(request, pk):
    booking = Booking.objects.get(id=pk)
    serializer = BookingSerializer(booking, many=False)
    return Response(serializer.data)
    
    