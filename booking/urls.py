from django.urls import path
from booking import views


urlpatterns = [
    #domain.com/home
    
    #home page booking site
    path('home/', views.home, name='home'),
    path('manage/', views.manage, name='manage'),
    path('manage/rooms', views.viewRooms, name='view-rooms'),
    path('manage/rooms/add', views.addRooms, name='add-rooms'),
    path('manage/booking', views.viewBookings, name='bookings'), # add booking
    
    
    
    
    path('', views.room_list, name='room_list'),
    path('book/<int:room_id>/', views.book_room, name='book_room')


]
