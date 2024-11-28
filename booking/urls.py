from django.urls import path
from booking import views


urlpatterns = [
    #domain.com/home
    
    #home page booking site
    path('home/', views.home, name='home'),

    #room manager actions
    path('manage/', views.manage, name='manage'),
    path('manage/rooms', views.viewRooms, name='view-rooms'),
    path('manage/rooms/add', views.addRooms, name='add-rooms'),
    path('manage/bookings', views.viewBookings, name='bookings'), # add booking
    path('manage/time-slot/<str:pk>', views.viewTimeSlots, name='view-timeslots'),
    path('manage/time-slots/add/<str:pk>', views.addTimeSlots, name='add-timeslots'),
    path('delete-timeslot/<str:pk>', views.deleteTimeSlot, name='delete-timeslot'),
    #user actions
    path('dashboard/', views.dashboard, name= 'dashboard'),
    path('available-rooms/<str:date>', views.availableRooms, name='available-rooms'),
    path('available-timeslots/<str:date>/<str:pk>', views.availableTimeSlots, name='available-timeslots'),
    path('room/<str:pk>', views.room, name='room'),
    path('user/bookings', views.userBookings, name='user-bookings'),
    path('user/profile', views.userProfile, name='user-profile'),
    path('book-room/<str:p_date>/<str:p>', views.bookRoom, name='book-room'),
    path('cancel-room/<str:ts>/<str:pk>', views.cancelRoom, name='cancel-room'),
    path('update-room/<str:pk>', views.updateRoom, name='update-room'),
    path('delete-room/<str:pk>', views.deleteRoom, name='delete-room'),
    
    

    
    
    
    
    

    
    

    
    
    
    
    path('', views.room_list, name='room_list'),
    path('book/<int:room_id>/', views.book_room, name='book_room')


]
