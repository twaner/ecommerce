from django.contrib import admin

# Register your models here.
from .models import Product, ProductImage, Variation, Category


class ProductAdmin(admin.ModelAdmin):
    readonly_fields = ['updated', 'timestamp']
    date_hierarchy = 'timestamp'
    list_editable = ['price', 'active']
    search_fields = ['title', 'description', 'active']
    list_display = ['title', 'price', 'active', 'updated']
    list_filter = ['price', 'active']
    prepopulated_fields = {'slug': ("title",)}

    class Meta:
        model = Product


class VariationAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "category",
        "product",
        "price",
        "active",
        "updated",
    ]

    class Meta:
        model = Variation

# Registrations

admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage)
admin.site.register(Variation, VariationAdmin)
admin.site.register(Category)

'''
 title = models.CharField(max_length=120, null=False, blank=False,)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2,default=29.99)
    slug = models.SlugField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    active = models.BooleanField(default=True)



from django.contrib import admin

# Register your models here.
from .models import Join


class JoinAdmin(admin.ModelAdmin):
    list_display = ['email', 'friend', 'timestamp', 'updated', 'ref_id']

    class Meta:
        model = Join

admin.site.register(Join, JoinAdmin)
# admin.site.register(JoinFriends)'''