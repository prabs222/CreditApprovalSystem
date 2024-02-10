# serializers.py

from rest_framework import serializers
from customers.models import Customer

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'age', 'monthly_salary', 'phone_number']

    def create(self, validated_data):
        approved_limit = round(36 * validated_data['monthly_salary'], -5)  # Rounded to nearest lakh
        validated_data['approved_limit'] = approved_limit
        validated_data['current_debt'] = 0
        return Customer.objects.create(**validated_data)
