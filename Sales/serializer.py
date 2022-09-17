from rest_framework import serializers
from .models import Sales
from Customers.serializer import CustomersSerializer
class SalesSerializer(serializers.ModelSerializer):
    customer_id=CustomersSerializer(
        many=False,
    )
    class Meta:
        model = Sales
        fields = '__all__'

