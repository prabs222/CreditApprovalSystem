# app/tasks.py

from celery import shared_task
from customers.management.commands.import_customers import Command as ImportCustomersCommand
from loans.management.commands.import_loans import Command as ImportLoansCommand

@shared_task
def import_customer_data():
    ImportCustomersCommand().handle()

@shared_task
def import_loan_data():
    ImportLoansCommand().handle()
