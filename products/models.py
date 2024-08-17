from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveIntegerField()
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name}-{self.rating}"

class FlashSale(models.Model):
    """Productlarga skidka funksiyasi"""
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    discount_percentage = models.PositiveIntegerField(help_text="Chegirma miqdorini kiriting:")  # Kiritilgan qiymatni % sifatida oladi, ya'ni: 15 --> 15% skidka
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        start_time_str = self.start_time.strftime('%d.%m.%Y %H:%M:%S')
        end_time_str = self.end_time.strftime('%d.%m.%Y %H:%M:%S')
        return f"{self.product.name} ga {start_time_str}dan {end_time_str} gacha {self.discount_percentage}% chegirma"

    def is_active(self):
        now = timezone.now
        return self.start_time <= now <= self.end_time

    class Meta:
        unique_together = ('product', 'start_time', 'end_time')


class ProductViewHistory(models.Model):
    """User tomonidan ko'rilgan productlarni vaqt asosida belgilaydi"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        time_stamp_str = self.timestamp.strftime('%d.%m.%Y %H:%M:%S')
        return f"{self.user} {self.product.name} ni {time_stamp_str} da ko'rgan "



