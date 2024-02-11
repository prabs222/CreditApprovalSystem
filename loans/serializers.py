from customers.models import Customer
from datetime import date
from rest_framework import serializers
from loans.models import Loan

class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = '__all__'

class CreateLoanSerializer(serializers.ModelSerializer):
    customer_id = serializers.IntegerField()
    class Meta:
        model = Loan
        fields = ['customer_id','loan_amount','interest_rate','tenure'] 
        
class LoanDetailSerializer(serializers.ModelSerializer):
    repayments_left = serializers.SerializerMethodField()

    class Meta:
        model = Loan
        fields = ['loan_id', 'loan_amount', 'interest_rate', 'monthly_installment', 'repayments_left']
    def get_repayments_left(self, obj):
        start_date = obj.start_date
        today = date.today()
        months_passed = (today.year - start_date.year) * 12 + (today.month - start_date.month)
        repayments_left = max(0, obj.tenure - months_passed)
        return repayments_left

class CustomerDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['customer_id', 'first_name', 'last_name', 'phone_number', 'age']

class LoanDetailForCustomerSerializer(serializers.ModelSerializer):
    customer = CustomerDetailSerializer(source='customer_id')
    
    class Meta:
        model = Loan
        fields = ['loan_id', 'loan_amount', 'interest_rate', 'monthly_installment', 'tenure', 'customer']
