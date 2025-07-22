from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Product, Category,User,Cart,CartItem

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(User)
admin.site.register(Cart)
admin.site.register(CartItem)