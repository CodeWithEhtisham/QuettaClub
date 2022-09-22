from rest_framework import serializers
from .models import Sales, Bill
from Customers.serializer import CustomersSerializer

class SalesSerializer(serializers.ModelSerializer):
    customer_id=CustomersSerializer(
        many=False,
    )
    class Meta:
        model = Sales
        fields = '__all__'

class BillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bill
        fields = '__all__'
