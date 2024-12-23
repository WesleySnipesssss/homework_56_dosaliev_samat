from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="Наименование")
    description = models.TextField(blank=True, verbose_name="Описание")

    def __str__(self):
        return self.name

class Product(models.Model):
    title = models.CharField(max_length=255, unique=True, verbose_name="Наименование")
    description = models.TextField(blank=True, verbose_name="Описание")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата и время добавления")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Стоимость")
    image = models.ImageField(upload_to='products/', verbose_name="Изображение")

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Стоимость",
        validators=[MinValueValidator(0.01)]
    )
    stock = models.IntegerField(
        default=0,
        verbose_name="Остаток",
        validators=[MinValueValidator(0)]
    )

    def __str__(self):
        return self.title

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carts')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart of {self.user}"

class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"

class Order(models.Model):
    user_name = models.CharField(max_length=100, verbose_name="Имя пользователя")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    address = models.CharField(max_length=255, verbose_name="Адрес")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата и время создания")

    def __str__(self):
        return f"Заказ {self.id} от {self.user_name}"

    class Meta:
        ordering = ['-created_at']


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, related_name='order_products', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_products', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество")

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    class Meta:
        verbose_name = "Продукт в заказе"
        verbose_name_plural = "Продукты в заказе"