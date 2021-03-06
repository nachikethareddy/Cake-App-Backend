from rest_framework import serializers
from .models import (
    CakeDepartment,
    CakeShopDetails,
    UserCakeShopRelationship,
    Cakes,
    Flavors,
    OrderCake,
    UserOccasion,
    CakeShopDetails,
    OrderProcessing,
    PhotoCakeLogger
)


class CakeShopDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CakeShopDetails
        fields = '__all__'

class UserCakeShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCakeShopRelationship
        fields = '__all__'

class CakeDepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CakeDepartment
        fields = '__all__'

class FlavoursSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flavors
        fields = "__all__"
        depth = 1


class CakeSerializer(serializers.ModelSerializer):
    flavours = serializers.SerializerMethodField()
    class Meta:
        model = Cakes
        fields = '__all__'
    def get_flavours(self, obj):
        return FlavoursSerializer(Flavors.objects.filter(cake=obj.id), many=True).data


class OrderCakeSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderCake
        exclude = ['occasion_root']

class OrderCakeAdminSerializer(serializers.ModelSerializer):
    order_details = serializers.SerializerMethodField()
    photos = serializers.SerializerMethodField()
    cake_name = serializers.CharField(source='cake_details.cake_name')
    cake_department = serializers.CharField(source='cake_details.cake_department.department_name')
    class Meta:
        model = OrderCake
        exclude = ['occasion_root']
        depth = 1 
    def get_order_details(self, obj):
        return OrderProcessingSerializer(OrderProcessing.objects.filter(order=obj.id), many=True).data

    def get_photos(self,obj):
        return PhotoCakeLoggerSerializer(PhotoCakeLogger.objects.filter(order=obj.id),many=True).data


class PhotoCakeLoggerSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhotoCakeLogger
        fields = '__all__'
        

class UserOccasionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserOccasion
        fields = '__all__'

class OrderProcessingSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProcessing
        fields = '__all__'



class DatabaseAdminSerializer(serializers.ModelSerializer):
    occasion = serializers.CharField(source='occasion_root.occasion')
    class Meta:
        model = OrderCake
        fields = '__all__'


class UserCakeShopAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCakeShopRelationship
        fields = '__all__'
        depth = 1