#admin.py
from django.contrib import admin
from .models import Category, Shoe, Order ,Cart, CartItem

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent_category')

class shoeAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'size', 'category')
    list_filter = ('category',)

class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'shoe', 'quantity')

class CartAdmin(admin.ModelAdmin):
    list_display = ('user',)

class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'shoe', 'quantity')

admin.site.register(Category, CategoryAdmin)
admin.site.register(Shoe, shoeAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
