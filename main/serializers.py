from rest_framework import serializers
from .models import FuelSupply, User, Category, Item, Station, Order, Remittance, Truck, Store

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class TruckSerializer(serializers.ModelSerializer):
    class Meta:
        model = Truck
        fields = '__all__'

class ItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    class Meta:
        model = Item
        fields = '__all__'

class StationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        fields = '__all__'

class SupplySerializer(serializers.ModelSerializer):
    truck = TruckSerializer(read_only=True)
    station = StationSerializer(read_only=True)
    station_id = serializers.PrimaryKeyRelatedField(source="station", queryset=Station.objects.all(), write_only=True)
    truck_id = serializers.PrimaryKeyRelatedField(source="truck", queryset=Truck.objects.all(), write_only=True)
    
    class Meta:
        model = FuelSupply
        fields = '__all__'
        
class RemittanceSerializer(serializers.ModelSerializer):
    supply = SupplySerializer(read_only=True)
    class Meta:
        model = Remittance
        fields = '__all__'

class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    store = StoreSerializer(read_only=True)
    truck = TruckSerializer(read_only=True)
    item = ItemSerializer(read_only=True)
    
    class Meta:
        model = Order
        fields = '__all__'
