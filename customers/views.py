from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from customers.serializers import CustomerSerializer

class RegisterCustomer(APIView):
    def post(self, request):
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # This will call the create method of the serializer
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

'''
Field: Value
customer_id: Id of customer (int)
approval: can loan be approved (bool)
interest_rate: Interest rate on loan (float)
corrected_interest_rate: Corrected Interest Rate based on credit rating, same as interest rate if the interest rate matches the slab (float) 
tenure: Tenure of loan (int)
monthly_installment:Monthly installment to be paid as repayment (float)
'''

"first_name"
"last_name"
"age"
"monthly_income"
"phone_number"