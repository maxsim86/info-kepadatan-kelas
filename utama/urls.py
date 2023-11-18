# urls.py
from django.urls import path
from .views import InfoListView, InfoFilterView, InfoSelectView

urlpatterns = [
    path('items/', InfoListView.as_view(), name='item_list'),
    path('items/filter/', InfoFilterView.as_view(), name='item_filter'),
    path('items/select_info/', InfoSelectView.as_view(), name='select_view'),
    # tambahkan url lain sesuai kebutuhan
]
