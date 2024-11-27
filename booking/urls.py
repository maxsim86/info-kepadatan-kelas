from django.urls import path
from booking import views


urlpatterns = [
    path('room_list/', views.room_list, name='room_list'),
    path('book/<int:room_id>/', views.book_room, name='book_room')
]
