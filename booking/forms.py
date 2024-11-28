from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import Room, TimeSlot, Booking

class RoomForm(forms.ModelForm):
    class Meta;
    model = Room
    fields = ('name', 'advance_booking' )