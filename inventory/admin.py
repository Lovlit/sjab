from django.contrib import admin
from .models import Category, Warehouse, Item, ItemWarehouseMapping, Voucher, VoucherItemMapping


class ItemAdmin(admin.ModelAdmin):
    ordering = ['name']
    # autocomplete_fields = ['category']
    search_fields = ['name',]
    list_filter = ('category',)
    raw_id_fields = ("category",)


class ItemWarehouseMappingAdmin(admin.ModelAdmin):
    ordering = ['warehouse']
    list_filter = ('warehouse',)
    list_display = ['warehouse','item', 'stock']
    search_fields = ['stock']




# Register your models here.
admin.site.register(Category)
admin.site.register(Warehouse)
admin.site.register(Item, ItemAdmin)
admin.site.register(ItemWarehouseMapping, ItemWarehouseMappingAdmin)
admin.site.register(Voucher)
admin.site.register(VoucherItemMapping)
