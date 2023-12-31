from django.db import models
from django.utils.text import slugify
from django.urls import reverse

from shop.utils import random_slug


class Category(models.Model):
    """
    Represents a category in the database.

    """
    name = models.CharField('Название категории',max_length=128, db_index=True, unique=True, )
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True, related_name='children', 
        verbose_name='Родительская категория'
        )
    slug = models.SlugField('URL', max_length=128, db_index=True, unique=True, null=False)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        unique_together = ('slug', 'parent')
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        """
        Return a string representation of the object.
        """
        full_path = [self.name]
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent
        return ' -> '.join(full_path[::-1])
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(random_slug() + '-name:' + self.name)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse("shop:categories-list", kwargs={"slug": self.slug})
        

class Product(models.Model):
    """
    Represents a product in the database.

    """
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория', related_name='products')
    title = models.CharField('Наименование', max_length=128)
    brand = models.CharField('Бренд', max_length=128)
    description = models.TextField('Описание', blank=True)
    slug = models.SlugField('URL', max_length=128)
    price = models.DecimalField('Цена', max_digits=8, decimal_places=2, default=0)
    image = models.ImageField('Изображение', upload_to='products/products/%Y/%m/%d', blank=True)
    available = models.BooleanField('Доступен для заказа', default=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:        
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        """
        Return a string representation of the object.
        """
        return self.title
    
    def get_absolute_url(self):
        return reverse("shop:product-detail", kwargs={"slug": self.slug})


class ProductManager(models.Manager):
    def get_queryset(self):
        """
        Return a queryset of available products.

        Returns:
            QuerySet: A filtered queryset of available products.
        """
        return super(ProductManager, self).get_queryset().filter(available=True)


class ProductProxy(Product):
    """
    A proxy model that extends the base `Product` model.
    This class defines a proxy model called `ProductProxy` that inherits from the `Product` model. It allows you to define additional methods or override existing methods without modifying the original `Product` model.
  
    """

    objects = ProductManager()

    class Meta:
        proxy = True 