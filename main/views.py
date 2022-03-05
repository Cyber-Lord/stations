from django import views
from django.shortcuts import render
from django.core.serializers import serialize
from main.serializers import StoreSerializer
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.decorators import action, permission_classes
from rest_framework import status
from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder

from .models import Category, FuelSupply, Item, Order, Remittance, Station, Truck, User, Store, PENDING, APPROVED, REJECTED
from .serializers import ItemSerializer, OrderSerializer, RemittanceSerializer, StationSerializer, SupplySerializer, TruckSerializer, UserSerializer, CategorySerializer

supported_http_method_names = ['get', 'post', 'patch', 'delete', 'put']

# Create your views here.
class CategoryViewSet(ModelViewSet):
    http_method_names = supported_http_method_names
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

class ItemViewSet(ModelViewSet):
    http_method_names = supported_http_method_names
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        return {'request': self.request}

    def delete(self, request, pk):
        item = get_object_or_404(Item, pk=pk)
        if Item.orderitems.count() > 0:
            return Response({'error': 'Product cannot be deleted because it is associated with an order item.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class StationViewSet(ModelViewSet):
    http_method_names = supported_http_method_names
    queryset = Station.objects.all()
    serializer_class = StationSerializer
    permission_classes = [IsAuthenticated]

class TruckViewSet(ModelViewSet):
    queryset = Truck.objects.all()
    serializer_class = TruckSerializer
    permission_classes = [IsAuthenticated]

class RemittanceViewSet(ModelViewSet):
    http_method_names = supported_http_method_names
    queryset = Remittance.objects.exclude(Q(status=APPROVED) | Q(status=REJECTED))
    serializer_class = RemittanceSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = self.queryset
        if self.request.user.is_superuser:
            return self.queryset

        query_set = Remittance.objects.filter(supply__station__station_manager_id=self.request.user.id).order_by("-timestamp")
        return query_set

class OrderViewSet(ModelViewSet):
    http_method_names = supported_http_method_names
    queryset = Order.objects.filter(order_status=PENDING).order_by('-order_date')
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = self.queryset
        if self.request.user.is_superuser:
            return self.queryset

        query_set = Order.objects.filter(store__manager_id=self.request.user.id).order_by("-order_date")
        return query_set

class StoreViewSet(ModelViewSet):
    http_method_names = supported_http_method_names
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    permission_classes = [IsAuthenticated]

class SupplyViewSet(ModelViewSet):
    http_method_names = supported_http_method_names
    queryset = FuelSupply.objects.all()
    serializer_class = SupplySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = self.queryset
        if self.request.user.is_superuser:
            return self.queryset

        query_set = FuelSupply.objects.filter(station__station_manager_id=self.request.user.id).order_by("-timestamp")
        return query_set

class UserViewSet(ModelViewSet):
    http_method_names = supported_http_method_names
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

    @action(detail=True, permission_classes=[IsAuthenticated])
    def history(self, request, pk):
        return Response('Ok')

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated()]

    @action(detail=False, methods=['GET','PUT'], permission_classes=[IsAuthenticated])
    def me(self, request):
        user = User.objects.get(user_id=request.user.id)
        if request.method == 'GET':
            serializer = UserSerializer(user)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = User(user, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

class RangeViewSet(views.View):
    def get(self, request):
        reportType = request.GET.get("report_type")
        from_ = request.GET.get("from")
        to = request.GET.get("to")
        qs = Remittance.objects.none()
        if not all([reportType, from_, to]):
            return JsonResponse({"Error": "please pass the required params"})

        if reportType == 'store':
            qs = Order.objects.filter(order_date__range=[from_, to])
            serializer = OrderSerializer(qs, many=True)
    
        if reportType == 'station':
            qs = Remittance.objects.filter(timestamp__range=[from_, to])
            serializer = RemittanceSerializer(qs, many=True)

        return JsonResponse(serializer.data, safe=False)