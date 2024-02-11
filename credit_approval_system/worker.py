from loans.models import Loan
from celery import shared_task
from customers.models import Customer
import pandas as pd
from credit_approval_system.celery import app

@shared_task
def import_customer_data():
    customer_data = pd.read_excel('static/customer_data.xlsx')
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

@shared_task
def import_loan_data():
    loan_data = pd.read_excel('static/loan_data.xlsx')
    for index, row in loan_data.iterrows():
        customer_id = row['Customer ID']
        loan_id = row['Loan ID']  
        loan_amount = row['Loan Amount']
        end_date = row['End Date']

        customer = Customer.objects.get(customer_id=customer_id)
        if Loan.objects.filter(loan_id=loan_id).exists():
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

        if is_loan_active(end_date):
            update_customer_current_debt(customer_id, loan_amount)

def is_loan_active(end_date):
    end_date_date = end_date.date()
    today_date = pd.Timestamp.now().date()
    return end_date_date > today_date

def update_customer_current_debt(customer_id, loan_amount):
    customer = Customer.objects.get(customer_id=customer_id)
    customer.current_debt += loan_amount
    customer.save()

