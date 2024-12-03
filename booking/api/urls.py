from django.urls import path
from booking import views

urlpatterns = [
    path('', views.getRouters),
    path('users/', views.getRoutes),
]
