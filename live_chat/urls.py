from django.urls import path
from . views import * 

urlpatterns = [
    path('chat/', views.chat_view, name='home')
 ]
