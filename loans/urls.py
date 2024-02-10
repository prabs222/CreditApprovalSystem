from django.urls import path
from .views import *

urlpatterns = [
    path('check-eligibility/', CheckEligibility.as_view(), name='check_eligibility'),
    path('create-loan/', CreateLoan.as_view(), name='create_loan'),
    path('view-loan/<int:loan_id>', ViewLoan.as_view(), name='view_loan'),
    path('view-loans/<int:customer_id>', ViewLoansByCustomer.as_view(), name='view_loans'),
]

{
"customer_id": 14,
"loan_amount": 50000,
"interest_rate": 7,
"tenure": 16
}