# urls.py
from django.urls import path
from .views import  *

urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('register/', RegisterCustomer.as_view(), name='register_customer'),
    path('trigger-import/', FillDataView.as_view(), name='trigger_import_loan'),
]
