# urls.py
from django.urls import path
from .views import InfoListView, InfoFilterView

urlpatterns = [
    path('items/', InfoListView.as_view(), name='item_list'),
    path('items/filter/', InfoFilterView.as_view(), name='item_filter'),
    # tambahkan url lain sesuai kebutuhan
]
