from rest_framework import serializers
from .models import Customer, Driver, Vehicle, Schedule, Issue, Collection

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
    


    

class DriverSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only = True)
    password2 = serializers.CharField(write_only = True)


    class Meta:
        model = Driver
        fields = ['other_names', 'last_name', 'driver_license_number','mobile_phone' , 'email', 'date_of_birth', 'password1', 'password2']



        def validate(self, data):
            if data['password1'] != data['password2']:
                raise serializers.ValidationError('The passwords do not match')
            return data
        

        def create(self, validated_data):
            validated_data.pop('password2')
            password = validated_data.pop('password1')
            driver = Driver.objects.create(**validated_data)
            driver.set_password(password)
            driver.save()
            return 
        


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = '__all__'



class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = '__all__'



class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = '__all__'



class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = '__all__'

