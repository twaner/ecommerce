from django.core.urlresolvers import reverse
from django.db import models

# Create your models here.


class Category(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField(null=True, blank=True)
    featured = models.BooleanField(default=False)
    slug = models.SlugField(unique=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=120, null=False, blank=False,)
    description = models.TextField(null=True, blank=True)
    category = models.ManyToManyField(Category, null=True, blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=29.99)
    saleprice = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    slug = models.SlugField(unique=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    class Meta:
        unique_together = ('title', 'slug')

    def get_price(self):
        return self.price

    def get_absolute_url(self):
        return reverse('single_product', kwargs={"slug": self.slug}) #args=[self.slug']


class ProductImage(models.Model):
    product = models.ForeignKey(Product)
    image = models.ImageField(upload_to='product/images/', null=True, blank=True)
    featured = models.BooleanField(default=False)
    thumbnail = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.product.title


class VariationManager(models.Manager):
    def all(self):
        return super(VariationManager, self).filter(active=True)

    def sizes(self):
        return self.all().filter(category='size')

    def colors(self):
        return self.all().filter(category='color')


VAR_CATEGORIES = (
    ('size', 'size'),
    ('color', 'color'),
    ('package', 'package'),
)


class Variation(models.Model):
    title = models.CharField(max_length=120)
    category = models.CharField(max_length=120, choices=VAR_CATEGORIES, default='size')
    product = models.ForeignKey(Product)
    price = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=2)
    image = models.ForeignKey(ProductImage, null=True, blank=True)
    active = models.BooleanField(default=True)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    objects = VariationManager()

    def __str__(self):
        return self.title