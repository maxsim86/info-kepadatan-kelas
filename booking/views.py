from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Room
from datetime import datetime
import requests


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

def viewRooms(request):
    rooms = Room.objects.all()
    total_rooms = len(rooms)


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
