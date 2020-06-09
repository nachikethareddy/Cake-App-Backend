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
    CakeShopDetails,
    UserOccasion,
    OrderProcessing
)

from .serializers import (
    CakeDepartmentSerializer,
    CakeSerializer,
    OrderCakeSerializer,
    UserOccasionSerializer,
    CakeShopDetailsSerializer,
    UserCakeShopSerializer,
    OrderCakeAdminSerializer,
    OrderProcessingSerializer
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
        query = Cakes.objects.filter(cake_department=id)
        serailzer = CakeSerializer(query,many=True)
        return Response({
            'status':'success',
            'payload':serailzer.data
        },status=200)



class PostOrder(APIView):
    parsers = [JSONParser]
    permissions = [permissions.IsAuthenticated]
    def post(self,request):
        serializer = OrderCakeSerializer(data=request.data)
        serializer1 = UserOccasionSerializer(data=request.data)
        if serializer1.is_valid():
            serializer1.save()
            if  serializer.is_valid():
                serializer.save(occasion_root=UserOccasion.objects.filter(id=serializer1.data['id'])[0])
                return Response({
                    'status':'success',
                    'payload':serializer.data
                },status=201)
        return Response({
            'status':'failed',
            'error':serializer1.errors,
            'error1':serializer.errors,
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
                serailiaer = UserCakeShopSerializer(obejcts,many=True)
                return Response({
                    "message":"User Logged In", 
                    "cake_shop_details":serailiaer.data,
                    "token":token.key,
                })
            else:
                return Response(status=403)



class AdminLogin(APIView):
    permission_classes = (permissions.AllowAny,)
    parser_classes = [JSONParser]
    def post(self, request):
        req_data = request.data
        user = authenticate(username=req_data['username'], password=req_data['password'])
        if not user:
            return Response({"message":"Invalid Details"}, status=400)
        else:
            token, _ = Token.objects.get_or_create(user=user)
            obejcts = CakeShopDetails.objects.filter(user=user)
            if obejcts.count() > 0:
                serailiaer = CakeShopDetailsSerializer(obejcts,many=True)
                return Response({
                    "message":"User Logged In", 
                    "cake_shop_details":serailiaer.data,
                    "token":token.key,
                })
            else:
                return Response(status=403)


class AdminPendingCakes(APIView):
    permission_classes = (permissions.AllowAny,)
    parser_classes = [JSONParser]
    def get(self,request):
        user = CakeShopDetails.objects.filter(user=request.user)
        if user.count()>0:
            objects = OrderCake.objects.filter(order_status=0).filter(cake_details__cake_department__cake_shop__id=user[0].id)
            serializer = OrderCakeAdminSerializer(objects,many=True)
            return Response({
                'status':'success',
                'payload':serializer.data
            },status=200)
        else:
            return Response(status=403)
    
    def post(self,request):
        seralizer = OrderProcessingSerializer(data=request.data)
        if seralizer.is_valid():
            try:
                OrderCake.objects.filter(id=request.data['order']).update(order_status=1)
                seralizer.save()
                return Response({
                    'status':'done',
                    'payload':seralizer.data  
                    },status=201)
            except Exception as e:
                print(e)
                return Response(status=403)
        return Response({
            'status':'failed',
            'error':seralizer.errors,
        },status=400)


class AdminProccessingCakes(APIView):
    permission_classes = (permissions.AllowAny,)
    parser_classes = [JSONParser]

    def get_queryset_for_update(self,request,id):
        queryset = OrderProcessing.objects.filter(order=id)
        if queryset.exists():
            return True,queryset
        else:
            return False,"Object/Permssion doesn\'t exists!"

    def get(self,request):
        user = CakeShopDetails.objects.filter(user=request.user)
        if user.count()>0:
            objects = OrderCake.objects.filter(order_status=1).filter(cake_details__cake_department__cake_shop__id=user[0].id)
            serializer = OrderCakeAdminSerializer(objects,many=True)
            return Response({
                'status':'success',
                'payload':serializer.data
            },status=200)
        else:
            return Response(status=403)
    
    def post(self,request):
        id = request.data.get('order', None)
        if id is not None:
            status,queryset = self.get_queryset_for_update(request,id)
            if not status:
                return Response({
                        'message':'Object/Permssion doesn\'t exists!'
                    },status=404)
            else:
                seralizer = OrderProcessingSerializer(queryset[0],data=request.data,partial=True)
                if seralizer.is_valid():
                    try:
                        OrderCake.objects.filter(id=request.data['order']).update(order_status=2)
                        seralizer.save()
                        return Response({
                            'status':'done',
                            'payload':seralizer.data  
                            },status=201)
                    except Exception as e:
                        print(e)
                        return Response(status=403)
                return Response({
                    'status':'failed',
                    'error':seralizer.errors,
                },status=400)
        else:
            return Response({
                "status":"error",
                "message": "ID is a mandatory feild to pass",
                "payload": ""
                },status=403)