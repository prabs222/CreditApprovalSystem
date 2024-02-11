from celery import chain
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from customers.serializers import CustomerSerializer
from credit_approval_system.worker import import_customer_data, import_loan_data


class RegisterCustomer(APIView):
    def post(self, request):
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save() 
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FillDataView(APIView):
    def get(self, request):
        task_chain = chain(import_customer_data.si(), import_loan_data.si())

        task_chain.apply_async()
        return Response({'message': 'Data import task has been initiated'}, status=status.HTTP_201_CREATED)

class IndexView(APIView):
    def get(self, request):
        message = "Welcome to Credit Approval System"
        routes = [
        'GET /',
        'GET /trigger-import/',   
        'POST /register/',
        'GET /check-eligibility/',
        'POST /create-loan/',
        'GET /view-loan/<int:loan_id>/',
        'GET /view-loans/<int:customer_id>/',
    ]
        response = {"message": message, "routes": routes}
        return Response(response)