from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Room
from datetime import datetime
import requests

from .models import Room, Booking, TimeSlot


# Create your views here.
#Telegram bot token and chat ID

TELEGRAM_BOT_TOKEN = ''
TELEGRAM_CHAT_ID = ''


#homepage view
def home(request):
    return render(request, 'booking/base.html')



#room for manage page view
def manage(request):
    return render(request, 'booking/manage.html')
# Room
# add rooms page view
def addRooms(request):
    form = RoomForm()
    current_user = request.user
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('view-rooms')
    return render(request, 'booking/add_rooms.html', {'form':form,'user':current_user})

    
#Bookings
# view bookings page view
def viewBookings(request):
    all_bookings = Booking.objects.all()
    
    context = {"bookings": all_bookings}
    return render(request, 'booking/booking.html', context=context)
    











def viewRooms(request):
    rooms = Room.objects.all()
    total_rooms = len(rooms)

    context = {'rooms':rooms, 'total_rooms':total_rooms}
    return render(request, 'booking/view_room.html', context)


@login_required
def room_list(request):
    # get query from object
    rooms =Room.objects.all()
    return render(request, 'booking/room_list.html', {'rooms':rooms})


def book_room(request, room_id):
    if request.method =='POST':
        room = Room.objects.get(id=room_id)
        date = request.POST.get('date')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')

        #validate
        if Booking.objects.filter(room=room, date=date, start_time__lt=end_time, end_time__gt=start_time).exists():
            return JsonResponse({'success':False, 'message': 'slot already booking!'})

        #create new booking
        booking = Booking.objects.create(
            user = request.user,
            room=room,
            date=date,
            start_time=start_time,
            end_time=end_time,

        )
        # send notification to telegram
        message = (
            f"Booking Baru :\n"
                f"User : {request.user.username} \n"
                f"Bilik : {room.name}\n"
                f"Tarikh : {date}\n"
                f"Masa : {start_time}- {end_time}"
        )
        requests.post(
            f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
            data = {'chat_id': TELEGRAM_CHAT_ID, 'text':message}

        )

        return JsonResponse({ 'success': True })
    return render(request, 'booking/book_room.html', {'room_id':room_id})
