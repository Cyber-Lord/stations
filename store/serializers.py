from rest_framework import serializers
from .models import User, Category, Item, Station, Order, Remittance, Truck

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'is_superuser', 'last_login', 'first_name', 'last_name', 'other_name', 'phone', 'is_sales_person', 'is_store_keeper', 'is_station_manager']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title']

class TruckSerializer(serializers.ModelSerializer):
    class Meta:
        model = Truck
        fields = ['driver', 'number']

class ItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    class Meta:
        model = Item
        fields = ['name', 'category']

class StationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        fields = ['name', 'address', 'station_manager']
        
class RemittanceSerializer(serializers.ModelSerializer):
    truck = TruckSerializer()
    station = StationSerializer()
    class Meta:
        model = Remittance
        fields = ['id', 'station', "no_of_litres", 'status', 'rejection_note', 'truck', 'price_per_litre', 'teller', 'remittance_id', 'timestamp',]

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['truck', 'item', 'order_date', 'order_status']

