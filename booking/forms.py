from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import Room, TimeSlot, Booking
User = get_user_model()


class RegisterForm(forms.Form):
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Set Password",
                "class": "form-control",
            }
        )
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Confirm Password",
                "class": "form-control",
            }
        ),
    )

    class Meta:
        model = User
        fields = ["name", "email"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Your name",
                }
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "Your Email"}
            ),
        }


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ("name", "advance_booking")
        widget = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Room Name"}
            ),
            "advance_booking": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Advance booking days",
                    "type": "number",
                }
            ),
        }


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'email']
        widgets = {
            'name':forms.TextInput(attrs={'class':"form-control",
                                          }),
            'email':forms.EmailInput(attrs={'class': "form-control",})
        }
   
    
class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = {'name', 'advance_booking'}
        widgets = {
            'name':forms.TextInput(attrs={'class':"form-control", 'placeholder':' Room Name'}),
            'advance_booking': forms.NumberInput(attrs={'class':"form-control", 'placeholder': 'Advance booking days', 'type':"number"}),
            
        }
        def clean(self):
            cleaned_data = self.cleaned_data
            return cleaned_data