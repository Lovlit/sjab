from .models import Item, ItemWarehouseMapping
from django import forms


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = '__all__'


class ItemWarehouseForm(forms.ModelForm):
    class Meta:
        model = ItemWarehouseMapping
        fields = '__all__'

