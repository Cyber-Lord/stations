from django.contrib import admin, messages
from django.db.models.aggregates import Count
from django.db.models.query import QuerySet
from django.utils.html import format_html, urlencode
from django.urls import reverse
from . import models

admin.site.site_title = "AASalisu Admin"
admin.site.site_header = "AASalisu Management Console"

@admin.register(models.Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'category']
    list_filter = ['name']
    list_per_page = 10
    list_select_related = ['category']
    search_fields = ['name']

@admin.register(models.Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_filter = ['name']
    search_fields = ['name']

@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title']
    search_fields = ['title']

@admin.register(models.Truck)
class TruckAdmin(admin.ModelAdmin):
    list_display = ['driver']
    search_fields = ['number']

@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ['first_name', 'last_name',  'other_name', 'phone']
    search_fields = ['first_name__istartswith', 'last_name__istartswith']


    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            user_count=Count('username')
        )

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    def store(self, obj):
        return obj.store.name
        
    list_editable = ['order_status']
    list_display = [ 'store', 'order_status', 'item', 'order_date']

@admin.register(models.Station)
class StationAdmin(admin.ModelAdmin):
    list_display = ['name', 'address', 'station_manager']

@admin.register(models.Remittance)
class RemittanceAdmin(admin.ModelAdmin):
    list_display = ['supply', 'amount', 'status', 'timestamp']

@admin.register(models.FuelSupply)
class SupplyAdmin(admin.ModelAdmin):
    def station(self):
        return self.station.name
    
    list_display = ['station', 'truck', 'no_of_litres', 'price_per_litre', 'timestamp']