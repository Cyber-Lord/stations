from rest_framework import serializers
from .models import FuelSupply, User, Category, Item, Station, Order, Remittance, Truck

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
    category = CategorySerializer()
    class Meta:
        model = Item
        fields = '__all_'

class StationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        fields = '__all__'

class SupplySerializer(serializers.ModelSerializer):
    truck = TruckSerializer()
    station = StationSerializer()
    class Meta:
        model = FuelSupply
        fields = '__all__'
        
class RemittanceSerializer(serializers.ModelSerializer):
    supply = SupplySerializer()
    class Meta:
        model = Remittance
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

