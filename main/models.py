from statistics import mode
import string
from django.db import models
from django.forms import IntegerField
from .validators import ASCIIUsernameValidator
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator

from django.db import models

APPROVED = 'A'
PENDING = 'P'
REJECTED = 'R'

STATUS_CHOICES = [
    (APPROVED, 'Approved'),
    (PENDING, 'Pending'),
    (REJECTED, 'Rejected'),
]

class Category(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.title
    
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

class User(AbstractUser):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, blank=True)
    is_sales_person = models.BooleanField(default=False)
    is_store_keeper = models.BooleanField(default=False)
    is_station_manager = models.BooleanField(default=False)
    other_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(max_length=254, blank=True, null=True)

    username_validator = ASCIIUsernameValidator()

    def get_full_name(self):
        full_name = (
            f"{self.first_name or ''} {self.last_name or ''} {self.other_name or ''}"
        )
        if not full_name.strip(" "):
            return string.capwords(self.username)
        return string.capwords(full_name)
    
    def __str__(self):
        return self.get_full_name()


class Item(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name='categories')

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ['name']
        
class Truck(models.Model):
    number = models.CharField(max_length=15)
    driver = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.driver + " " + self.number

class Order(models.Model):
    truck = models.ForeignKey(Truck, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    order_status = models.CharField(
        max_length=1, choices=STATUS_CHOICES, default=PENDING)
    

class Station(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    station_manager = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return self.name


class FuelSupply(models.Model):
    station = models.ForeignKey(Station, on_delete=models.CASCADE)
    truck = models.ForeignKey(Truck, on_delete=models.CASCADE)
    no_of_litres = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    price_per_litre = models.FloatField()
    
    def __str__(self) -> str:
        return self.station.name
    
    class Meta:
        verbose_name = "Supply"
        verbose_name_plural = "Supplies"
    
class Remittance(models.Model):
    supply = models.ForeignKey(FuelSupply, on_delete=models.CASCADE)
    amount = models.DecimalField(
            max_digits=10,
            decimal_places=2,
            validators=[MinValueValidator(1)])
    status = models.CharField(choices=STATUS_CHOICES, max_length=15, default=PENDING)
    rejection_note = models.CharField(max_length=500, blank=True)
    teller = models.ImageField(upload_to='media/tellers', blank=True, null=True)
    remittance_id = models.CharField(max_length=10, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return f'Remittance - {self.remittance_id}'
    
    def save(self, *args, **kwargs):
        last_remittance = Remittance.objects.last()
        if not self.remittance_id:
            self.remittance_id = "#{0:05}".format((last_remittance.id if last_remittance else 0) + 1)
        super(Remittance, self).save(*args, **kwargs)
