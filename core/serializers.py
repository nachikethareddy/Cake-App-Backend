from rest_framework import serializers
from .models import (
    CakeDepartment,
    CakeShopDetails,
    UserCakeShopRelationship,
    Cakes,
    Flavors,
    OrderCake,
    UserOccasion,
    CakeShopDetails
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

class UserOccasionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserOccasion
        fields = '__all__'