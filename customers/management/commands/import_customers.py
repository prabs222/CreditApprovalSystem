from django.core.management.base import BaseCommand
from customers.models import Customer
import pandas as pd

class Command(BaseCommand):
    help = 'Import customer data from Excel file'

    def handle(self, *args, **kwargs):
        customer_data = pd.read_excel('customer_data.xlsx')
        for index, row in customer_data.iterrows():
            Customer.objects.create(
                first_name=row['First Name'],
                last_name=row['Last Name'],
                age=row['Age'],
                phone_number=row['Phone Number'],
                monthly_income=row['Monthly Salary'],
                approved_limit=row['Approved Limit'],
                current_debt=0  
            )
        self.stdout.write(self.style.SUCCESS('Customer data imported successfully'))
