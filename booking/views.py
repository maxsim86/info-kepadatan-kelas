from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Room
from datetime import datetime
import requests

from .forms import RoomForm, UserUpdateForm, RegisterForm
from .models import Room, Booking, TimeSlot
from datetime import datetime, date, timedelta


User = get_user_model()

#homepage view
def home(request):
    return render(request, 'booking/home.html')

    
#signin page view
def signinPage(request):
    page = 'signin'
    if request.method == 'POST':
        email = request.POST.get('email').lower() 
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email)
        except:
            messages.info(request, 'User doesnt exist !')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.info(request,  'Username or password doesnot exist')
    
    context = {'page':page}
    return render(request, 'booking/login_register.html', context)

    
# signup page view
def signupPage(request):
    page = 'signup'
    form = RegisterForm()
    context = {'page':page, 'form':form}

    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'An error occured!')
    return render(request, 'booking/login_register.html', context)
    

#sign out page
def signoutPage(request):
    logout(request)
    return render('signin')


#room page view
def room(request, pk):
    room_object = Room.objects.get(id=pk)
    context = {'room_object':room_object}
    return render(request, 'booking/room.html', context)

#booking logic
def bookRoom(request, p_date, pk):
    f_date = datetime.strptime(p_date, "%Y%m%d").date().strftime("%Y-%m-%d")
    user = User.objects.get(email=request.user)
    time_slot = TimeSlot.objects.get(id=pk)
    days = time_slot.room.advance_booking
    
    picked_date_obj  = datetime.strptime(f_date, "%Y-%m-%d")
    today_date_obj = date.today()

    try:
        booking_obj = Booking.objects.filter(user=user, time_slot=time_slot)
    except:
        print("Queryset doesn't exists") 

    if booking_obj.exists():
        message = 'AlREADY YOU'

    elif time_slot.booked == True:
        message = 'ALREADY'

    elif(picked_date_obj.day - today_date_obj>= days) and (time_slot.booked == False):
        TimeSlot.objects.filter(id=pk).update(booked=True)
        Booking.objects.create(user=user, time_slot=time_slot, date=f_date)
        message = 'SUCCESS'
    elif not((picked_date_obj.day - today_date_obj.day >= days) and (time_slot.booked == False)):
        message = 'FAILURE'
    
    elif not(picked_date_obj >= today_date_obj.day):
        message = 'ERROR'
    else:
        message = 'ERROR'
    
    context = {'user':user, 'time_slot':time_slot, 'message':message, 'days':days}
    return render(request, 'booking/book_room.html', context)
    
def cancelRoom(request, ts, pk):
    booking = Booking.objects.filter(id=pk)

    if request.method == 'POST':
        booking.delete()
        TimeSlot.objects.filter(id=ts).update(booked=False)
        return redirect('user-bookings')

    context={'booking':booking}
    return render(request, 'booking/cancel_room.html', context)
     
#for users
#dashboard page view
def dashboard(request):
    today = datetime.now()
    default_date = today.strftime("%Y-%m-%d")
    if request.method =='POST':
        picked_date = str(request.POST['date'])
        f_date = picked_date.replace('-', '')
        return redirect('available-rooms', f_date)
    context = {'today':default_date}
    return render(request, 'booking/dashboard.html', context)


#available room page view
def availableRooms(request, date):
    f_date = datetime.strptime(date, "%Y%m%d").date().strftime("%Y-%m-%d")
    rooms = Room.objects.all()
    context = {'rooms':rooms, 'date':f_date}
    
    return render(request, 'booking/available_room.html', context)

# available time slot page view
def availableTimeSlots(request, date, pk):
    room = Room.objects.get(id=pk)
    time_slots = TimeSlot.objects.filter(room=room)
    context = {'time_slot':time_slots, 'room':room, 'date':date}
    return render(request, 'booking/available_timeslots.html', context)



#user profile pageview
def userProfile(request):
    user = User.objects.get(email=request.user)
    form = UserUpdateForm(instance=user)
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile is updated successfully!')
        else:
            form = UserUpdateForm(instance=user)
    context = {'form':form}
    return render(request, 'booking/profile.html', context)

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



# delete room page view
def deleteRoom(request, pk):
    try:
        room = Room.objects.get (id=pk)
        context = {'room':room}
    except:
        context={'error':'an error occurred!'}

    if request.method == 'POST':
        room.delete()
        return redirect('view-rooms')
    return render(request, 'booking/delete.html', context)
        

# Timeslots
# Add Timeslot for room page view
def addTimeSlots(request, pk):
    room = Room.objects.get(id=pk)
    context = {'room':room}
    return render(request, 'booking/add_timeslots.html', context)


#view timeslots page view
def viewTimeSlots(request, pk ):
    room = Room.objects.get(id=pk)
    time_slots = TimeSlot.objects.filter(room=room)
    
    context = {'time_slots':time_slots, 'room':room}
    return render(request, 'booking/view_timeslots.html', context)
    
# delete timeslot page view
def deleteTimeSlot(request, pk):
    try:
        time_slot = TimeSlot.objects.get(id=pk)
        room = time_slot.room
        context = {'time_slot':time_slot}
    except:
        context = {'error': 'An Error Occured!'}
    
    if request.method=="POST":
        time_slot.delete()
        return redirect('view-timeslots', room.id)
    return render(request, 'base/delete_timeslot.html', context)
    
    


#Bookings
# view bookings page view
def viewBookings(request):
    all_bookings = Booking.objects.all()
    
    context = {"bookings": all_bookings}
    return render(request, 'booking/booking.html', context=context)
    
# view user bookings page view
def userBookings(request):
    user = User.objects.get(email=request.user)
    bookings = Booking.objects.filter(user=user)
    context = {'user ':user, 'booking':bookings}

    return render(request, 'booking/user_bookings.html', context)

def viewRooms(request):
    rooms = Room.objects.all()
    total_rooms = len(rooms)

    context = {'rooms':rooms, 'total_rooms':total_rooms}
    return render(request, 'booking/view_room.html', context)


def updateRoom(request, pk):
    room_object = Room.objects.get(id=pk)
    form = RoomForm(instance=room_object)
    
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room_object)
        if form.is_valid():
            form.save()
            return redirect('dashboard')

    context = {'form':form, 'room':room_object}
    return render(request, 'booking/update_room.html', context)
        

