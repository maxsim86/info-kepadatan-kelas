from django.urls import path
from . import views

urlpatterns = [
    path('', views.getRoutes),
    path('users/', views.getRoutes),
    path('users/<str:pk>/', views.getUsers),
    path('rooms', views.getRooms),
    path('rooms/<str:pk>/', views.getRoom),
    path('timeslots/', views.getTimeSlots),
    path('timeslots/<str:pk>/', views.getTimeSlot),
    path('bookings/', views.getBookings),
]
