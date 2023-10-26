from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


class Product(models.Model):
    product = models.CharField(max_length=60)
    description = models.TextField()
    images = models.ImageField(
        upload_to='product_images',
        default='default_image_product.png'
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.product


class Cart(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Корзина покупателя')
    products = models.ManyToManyField(Product, through='CartItem')

    def __str__(self):
        return str(self.customer)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, verbose_name='Корзина клиента')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')

    def __str__(self):
        return f'{str(self.product)} {str(self.cart)}'


class Category(models.Model):
    CATEGORY_CHOICES = [
        ('Смартфоны', 'Смартфоны'),
        ('Ноутбуки', 'Ноутбуки'),
        ('Мониторы', 'Мониторы'),
        ('Видеокарты', 'Видеокарты'),
        ('Другое', 'Другое'),
    ]

    name = models.CharField(max_length=100, choices=CATEGORY_CHOICES, default='Другое', verbose_name='Категория')
    description = models.TextField(blank=True, verbose_name='Описание')
    slug = models.SlugField(unique=True, blank=True, auto_created=True)

    # def save(self, *args, **kwargs):
    #     self.slug = slugify(self.name)
    #     super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
