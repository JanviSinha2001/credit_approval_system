# credit_app/serializers.py
from rest_framework import serializers
from .models import Customer, Loan

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class LoanSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()

    class Meta:
        model = Loan
        fields = '__all__'
