from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name='Name')
    slug = models.SlugField(max_length=50, blank=True, null=True, verbose_name='URL')
    created_at = models.DateTimeField(verbose_name='Date created', auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name='images')
    description = models.TextField(blank=True)
    price = models.CharField(max_length=20)
    created_at = models.DateTimeField(verbose_name='Date created', auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'


class ContactRequest(models.Model):
    first_name = models.CharField(max_length=40, verbose_name='First Name')
    lastname = models.CharField(max_length=40, verbose_name='Lastname')
    email = models.EmailField(verbose_name='Email')
    message = models.TextField(verbose_name='Message')
    created_at = models.DateTimeField(verbose_name='Date created', auto_now_add=True)

    def __str__(self):
        return f'{self.first_name} {self.lastname} {self.email}'

    class Meta:
        verbose_name = 'Message from contact form'
        verbose_name_plural = 'Messages from contact form'


class HomeSlider(models.Model):
    image = models.ImageField(upload_to='home/slider/', verbose_name='Photo')

    class Meta:
        verbose_name = 'Slider Photo'
        verbose_name_plural = 'Slider Photos'


class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments', verbose_name='Product')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', verbose_name='Author')
    text = models.TextField(verbose_name='Comment text')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Date created')

    def __str__(self):
        return f'{self.user.username} - {self.product.name}'

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites', verbose_name='user')
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='favorited_by', verbose_name='product')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='date of creation')

    class Meta:
        verbose_name = 'Favorite'
        verbose_name_plural = 'Favorites'
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.user.username} — {self.product.name}"




