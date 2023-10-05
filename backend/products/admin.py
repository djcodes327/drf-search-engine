from django.contrib import admin
from .models import Product


# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'user', 'public')
    list_editable = ('public',)


admin.site.register(Product, ProductAdmin)
