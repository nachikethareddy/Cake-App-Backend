from django.shortcuts import render

from rest_framework.parsers import JSONParser
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token

from .models import (
    CakeDepartment,
    CakeShopDetails,
    UserCakeShopRelationship,
    Cakes,
    OrderCake,
    CakeShopDetails
)

from .serializers import (
    CakeDepartmentSerializer,
    CakeSerializer,
    OrderCakeSerializer,
    UserOccasionSerializer,
    CakeShopDetailsDepartmentSerializer,
    UserCakeShopSerializer
)

class GetAllDepartment(APIView):
    parsers = [JSONParser]
    permissions = [permissions.IsAuthenticated]

    def get(self,request):
        try:
            cake_shop_id = request.user.usercakeshoprelationship.cake_shop.id
        except:
            return Response({
                'status':'failed'
            },status=401)
        query = CakeDepartment.objects.filter(cake_shop=cake_shop_id)
        serailzer = CakeDepartmentSerializer(query,many=True)
        return Response({
            'status':'success',
            'payload':serailzer.data
        },status=200)


class GetAllCakes(APIView):
    parsers = [JSONParser]
    permissions = [permissions.IsAuthenticated]
    def get(self,request,id):
        query = CakeDepartment.objects.filter(cake_shop=id)
        serailzer = CakeSerializer(query,many=True)
        return Response({
            'status':'success',
            'payload':serailzer.data
        },status=200)



class PostOrder(APIView):
    parsers = [JSONParser]
    permissions = [permissions.IsAuthenticated]
    def post(self,request,id):
        serializer = OrderCakeSerializer(data=request.data)
        serializer1 = UserOccasionSerializer(data=request.data)
        if serializer.is_valid() and serializer1.is_valid():
            serializer.save()
            serializer1.save()
            return Response({
                'status':'success',
                'payload':serializer.data
            },status=201)
        return Response({
            'status':'failed',
            'error':serializer.errors,
            'error1':serializer1.errors,
        },status=400)


class LoginView(APIView):
    permission_classes = (permissions.AllowAny,)
    parser_classes = [JSONParser]
    def post(self, request):
        req_data = request.data
        user = authenticate(username=req_data['username'], password=req_data['password'])
        if not user:
            return Response({"message":"Invalid Details"}, status=400)
        else:
            token, _ = Token.objects.get_or_create(user=user)
            obejcts = UserCakeShopRelationship.objects.filter(user=user)
            if obejcts.count() > 0:
                serailiaer = UserCakeShopRelationship(obejcts,many=True)
                return Response({
                    "message":"User Logged In", 
                    "cake_shop_details":serailiaer.data,
                    "token":token.key,
                })
            else:
                return Response(status=403)