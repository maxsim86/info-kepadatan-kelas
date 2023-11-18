# urls.py
from django.urls import path
from .views import InfoListView, InfoFilterView, InfoSelectView, StudentColorForm

urlpatterns = [
    path('items/', InfoListView.as_view(), name='item_list'),
    path('items/filter/', InfoFilterView.as_view(), name='item_filter'),
    path('items/select_info/', InfoSelectView.as_view(), name='select_view'),
    path('items/student_color/', StudentColorForm.as_view(), name='student_color'),
    # tambahkan url lain sesuai kebutuhan
]
