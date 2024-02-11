from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Customer

class RegisterCustomerTests(APITestCase):
    def test_register_customer_success(self):
        url = reverse('register-customer')
        data = {
            'first_name': 'Prabhakar',
            'last_name': 'Mishra',
            'age': 21,
            'monthly_income': 150000,
            'phone_number': 9794132207
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Customer.objects.count(), 1)
        self.assertEqual(Customer.objects.get().first_name, 'Prabhakar')
    
    def test_register_customer_invalid_data(self):
        url = reverse('register-customer')
        data = {
            'first_name': 'Prabhakar',
            'last_name': 'Mishra',
            'age': 21
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
