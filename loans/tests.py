from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Loan, Customer
from datetime import date, datetime, timedelta


class CheckEligibilityTests(APITestCase):
    def setUp(self):
        self.customer = Customer.objects.create(
            customer_id=1,
            first_name='John',
            last_name='Doe',
            age=30,
            monthly_income=5000,
            approved_limit=10000,
            current_debt=0,
            phone_number='1234567890'
        )

        self.loan = Loan.objects.create(
            customer_id=self.customer,
            loan_id=1,
            loan_amount=5000,
            tenure=12,
            interest_rate=5,
            monthly_installment=0,
            emis_paid_on_time=0,
            start_date=datetime.now(),
            end_date=datetime.now()
        )

    def test_check_eligibility_success(self):
        data = {
            'customer_id': 1,
            'loan_amount': 3000,
            'interest_rate': 5,
            'tenure': 12
        }
        url = reverse('check-eligibility')
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_check_eligibility_insufficient_funds(self):
        data = {
            'customer_id': 1,
            'loan_amount': 20000,
            'interest_rate': 5,
            'tenure': 12
        }

        url = reverse('check-eligibility')
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['approval'])
        self.assertEqual(response.data['reason'], 'Sum of current loans exceeds approved limit')

class ViewLoanTests(APITestCase):
    def setUp(self):
        self.customer = Customer.objects.create(
            first_name= 'Prabhakar',
            last_name= 'Mishra',
            age= 21,
            monthly_income= 150000,
            phone_number= 9794132207,
            approved_limit = 9870000
        )
        end_date = datetime.now().date() + timedelta(days=30 * 12)  
        
        self.loan = Loan.objects.create(
            customer_id=self.customer,
            loan_id=1234,
            loan_amount=1000.0,
            tenure=12,
            interest_rate=5.0,
            monthly_installment=100.0,
            emis_paid_on_time=0,
            end_date = end_date           
        )
    def test_view_existing_loan(self):
        """
        Test fetching an existing loan.
        """
        url = reverse('view-loan', args=[self.loan.loan_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['loan_id'], self.loan.loan_id)

    def test_view_nonexistent_loan(self):
        """
        Test fetching a loan that does not exist.
        """
        url = reverse('view-loan', args=[999])  
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class ViewLoansByCustomerTests(APITestCase):
    def setUp(self):
        self.customer = Customer.objects.create(
            customer_id=1,
            first_name='John',
            last_name='Doe',
            age=30,
            phone_number='1234567890',
            monthly_income=5000.0,
            approved_limit=20000.0,
            current_debt=0.0
        )

        self.loan1 = Loan.objects.create(
            customer_id=self.customer,
            loan_id=1234,
            loan_amount=1000.0,
            tenure=12,
            interest_rate=5.0,
            monthly_installment=100.0,
            emis_paid_on_time=0,
            end_date=date.today() + timedelta(days=30 * 12)
        )
        self.loan2 = Loan.objects.create(
            customer_id=self.customer,
            loan_id=5678,
            loan_amount=2000.0,
            tenure=6,
            interest_rate=6.0,
            monthly_installment=400.0,
            emis_paid_on_time=0,
            end_date=date.today() - timedelta(days=10) 
        )

    def test_get_loans_by_customer_success(self):
        url = reverse('view-loans', args=[1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1) 
        self.assertEqual(response.data[0]['loan_id'], self.loan1.loan_id)

    def test_get_loans_by_customer_invalid_customer(self):
        url = reverse('view-loans', args=[9999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

