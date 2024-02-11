from decimal import Decimal
import random
from django.db.models import Sum
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import date, datetime, timedelta
from .models import Loan, Customer
from .serializers import *


class CheckEligibility(APIView):
    def post(self, request):
        customer_id = request.data.get('customer_id')
        loan_amount = Decimal(request.data.get('loan_amount'))
        interest_rate = Decimal(request.data.get('interest_rate'))
        tenure = request.data.get('tenure')

        try:
            customer = Customer.objects.get(customer_id=customer_id)
            historical_loans = Loan.objects.filter(customer_id=customer_id)
        except Customer.DoesNotExist:
            return Response({"error": "Customer does not exist"}, status=status.HTTP_400_BAD_REQUEST)

        if customer.current_debt + loan_amount > customer.approved_limit:
            return Response({"approval": False, "reason": "Sum of current loans exceeds approved limit"}, status=status.HTTP_200_OK)

        credit_score = self.calculate_credit_score(customer, historical_loans)

        if credit_score < 10:
            approval = False
            corrected_interest_rate = None
            monthly_instalment = None
        else:
            approval = True
            corrected_interest_rate = self.calculate_interest_rate(credit_score,interest_rate)
        
        if approval:
            monthly_instalment = self.calculate_monthly_instalment(loan_amount, corrected_interest_rate, tenure)

        response_data = {
            "customer_id": customer_id,
            "approval": approval,
            "interest_rate": interest_rate,
            "corrected_interest_rate": corrected_interest_rate,
            "tenure": tenure,
            "monthly_instalment": monthly_instalment
        }

        return Response(response_data, status=status.HTTP_200_OK)

    def calculate_interest_rate(self,credit_score, interest_rate):
        if credit_score > 50:
            return interest_rate
        elif 30 < credit_score <= 50:
            return max(interest_rate, 12)
        elif 10 < credit_score <= 30:
            return max(interest_rate, 16)
            
            
    def calculate_credit_score(self, customer, historical_loans):
        credit_score = 0
        
        # i. Payment history
        payment_history_weight = 0.35
        total_on_time_payments = historical_loans.aggregate(total_on_time_payments=Sum('emis_paid_on_time'))['total_on_time_payments'] or 0
        total_tenure = historical_loans.aggregate(total_tenure=Sum('tenure'))['total_tenure'] or 0

        if total_tenure > 0:
            on_time_payment_percentage = (total_on_time_payments / total_tenure) * 100
            credit_score += on_time_payment_percentage * payment_history_weight

        # ii. No of loans taken in past
        loans_taken_weight = 0.15
        total_loans = historical_loans.count()
        credit_score += (1 - (total_loans / 10)) * loans_taken_weight

        # iii. Loan activity in current year
        if total_loans > 0:
            current_year_loans = historical_loans.filter(start_date__year=datetime.now().year)
            current_year_loan_count = current_year_loans.count()
            loan_activity_weight = 0.10
            credit_score += (1 - (current_year_loan_count / total_loans)) * loan_activity_weight

        credit_score = max(0, min(100, int(credit_score)))
        print("Credit Score: ", credit_score)
        return credit_score

    def calculate_monthly_instalment(self, loan_amount, interest_rate, tenure):
        if loan_amount is None or interest_rate is None or tenure is None:
            raise ValueError("One or more input parameters are missing or invalid")

        principal = loan_amount
        monthly_interest_rate = Decimal((interest_rate / 100) / 12 )
        loan_term_months = tenure
        monthly_instalment = (principal * monthly_interest_rate * pow(1 + monthly_interest_rate, loan_term_months)) / (pow(1 + monthly_interest_rate, loan_term_months) - 1)

        return monthly_instalment

class CreateLoan(APIView):
    def generate_loan_id(self):
        return random.randint(1000, 9999)

    def post(self, request):
        serializer = CreateLoanSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        customer_id = serializer.validated_data.get('customer_id')
        loan_amount = serializer.validated_data.get('loan_amount')
        interest_rate = serializer.validated_data.get('interest_rate')
        tenure = serializer.validated_data.get('tenure')

        try:
            customer = Customer.objects.get(customer_id=customer_id)
        except Customer.DoesNotExist:
            return Response({'message': 'Customer does not exist'}, status=status.HTTP_404_NOT_FOUND)

        check_eligibility = CheckEligibility()
        response = check_eligibility.post(request)
        
        loan_approved = response.data["approval"]
        corrected_interest_rate = response.data["corrected_interest_rate"]
        monthly_installment = response.data["monthly_instalment"]

        if loan_approved:
            while True:
                loan_id = self.generate_loan_id()
                if not Loan.objects.filter(loan_id=loan_id).exists():
                    break
            current_date = datetime.now().date()
            end_date = current_date + timedelta(days=30 * tenure)
            try:
                with transaction.atomic():
                    loan = Loan.objects.create(
                        customer_id=customer,
                        loan_id=loan_id,
                        loan_amount=loan_amount,
                        interest_rate=corrected_interest_rate,
                        tenure=tenure,
                        monthly_installment=monthly_installment,
                        emis_paid_on_time=0,
                        end_date=end_date
                    )
            except Exception as e:
                return Response({'message': f"Something went wrong! Looks like this: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            message = 'Loan approved. Monthly installment calculated.'
        else:
            loan_id = None
            message = 'Loan not approved. Eligibility criteria not met.'

        response_data = {
            'loan_id': loan_id,
            'customer_id': customer_id,
            'loan_approved': loan_approved,
            'message': message,
            'monthly_installment': monthly_installment
        }
        return Response(response_data, status=status.HTTP_200_OK)


class ViewLoan(APIView):
    def get(self, request, loan_id):
        try:
            loan = Loan.objects.get(loan_id=loan_id)
            serializer = LoanDetailForCustomerSerializer(loan)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Loan.DoesNotExist:
            return Response({'message': 'Loan not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': f"Something went wrong: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ViewLoansByCustomer(APIView):
    def get(self, request, customer_id):
        try:
            loans = Loan.objects.filter(customer_id=customer_id, end_date__gte=date.today())
            loan_serializer = LoanDetailSerializer(loans, many=True)
            return Response(loan_serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': f"Something went wrong: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)