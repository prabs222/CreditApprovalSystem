from django.core.management.base import BaseCommand
from loans.models import Loan
from customers.models import Customer
import pandas as pd

class Command(BaseCommand):
    help = 'Import loan data from Excel file'

    def handle(self, *args, **kwargs):
        loan_data = pd.read_excel('loan_data.xlsx')
        for index, row in loan_data.iterrows():
            customer_id = row['Customer ID']
            loan_id = row['Loan ID']  
            loan_amount = row['Loan Amount']
            end_date = row['End Date']

            customer = Customer.objects.get(customer_id=customer_id)
            if Loan.objects.filter(loan_id=loan_id).exists():
                self.stdout.write(self.style.WARNING(f"Loan ID {loan_id} already exists. Skipping creation."))
                continue

            loan = Loan.objects.create(
                customer_id=customer,
                loan_id=loan_id,
                loan_amount=loan_amount,
                tenure=row['Tenure'],
                interest_rate=row['Interest Rate'],
                monthly_installment=row['Monthly payment'],
                emis_paid_on_time=row['EMIs paid on Time'],
                start_date=row['Date of Approval'],
                end_date=end_date
            )

            if self.is_loan_active(end_date):
                self.update_customer_current_debt(customer_id, loan_amount)

        self.stdout.write(self.style.SUCCESS('Loan data imported successfully'))

    def is_loan_active(self, end_date):
        end_date_date = end_date.date()
        today_date = pd.Timestamp.now().date()
        return end_date_date > today_date

    def update_customer_current_debt(self, customer_id, loan_amount):
        customer = Customer.objects.get(customer_id=customer_id)
        customer.current_debt += loan_amount
        customer.save()
