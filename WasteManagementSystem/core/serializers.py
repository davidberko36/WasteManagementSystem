from rest_framework import serializers
from .models import Customer

class CustomerSerializer (serializers.ModelSerializer):
    password1 = serializers.CharField(write_only = True)
    password2 = serializers.CharField(write_only = True)


    class Meta:
        model = Customer
        fields = ['customer_id', 'other_name', 'last_name', 'address', 'email', 'mobile_phone', 'username', 'date_of_birth', 'user_type','password1', 'password2']


    def validate(self, data):
        if data ['password1'] != data['password2']:
            raise serializers.ValidationError('The passwords do not match')
        return data
    

    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password1')
        customer = Customer.objects.create(**validated_data)
        customer.set_password(password)
        customer.save()
        return customer