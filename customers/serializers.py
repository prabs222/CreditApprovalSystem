# serializers.py

from rest_framework import serializers
from customers.models import Customer

class CustomerSerializer(serializers.ModelSerializer):
    approved_limit = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()

    class Meta:
        model = Customer
        fields = ['customer_id', 'first_name','last_name','name', 'age', 'monthly_income', 'phone_number', 'approved_limit']

    def create(self, validated_data):
        approved_limit = round(36 * validated_data['monthly_income'], -5)  
        validated_data['approved_limit'] = approved_limit
        validated_data['current_debt'] = 0
        customer = Customer.objects.create(**validated_data)
        return customer

    def get_name(self, obj):
        first_name = getattr(obj, 'first_name', '')
        last_name = getattr(obj, 'last_name', '')
        return f"{first_name} {last_name}"

    def get_approved_limit(self, obj):
        return round(36 * obj.monthly_income, -5)
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['name'] = self.get_name(instance) 
        data['customer_id'] = instance.customer_id
        data.pop('first_name', None)
        data.pop('last_name', None)
        return data
