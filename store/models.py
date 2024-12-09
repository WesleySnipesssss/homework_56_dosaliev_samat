from django.db import models
from django.core.validators import MinValueValidator

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