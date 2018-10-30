from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.


class Warehouse(models.Model):
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.name


class Item(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.name


class ItemWarehouseMapping(models.Model):
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    stock = models.IntegerField()

    def __str__(self):
        return '{}: {} , {}'.format(self.warehouse.name, self.item.name, self.stock)


class Voucher(models.Model):
    voucher_number = models.BigIntegerField(unique=True, auto_created=True, null=True, blank=True)
    issued_by = models.CharField(max_length=30)
    issued_to = models.CharField(max_length=30)
    date_issued = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}: {}'.format(self.voucher_number, self.date_issued)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if not self.voucher_number:
            self.voucher_number = Voucher.objects.filter().last().id + 1
            super(Voucher, self).save()


class VoucherItemMapping(models.Model):
    voucher_number = models.ForeignKey(Voucher, on_delete=models.CASCADE, unique=True)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    # category = models.ForeignKey(Category, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE,)
    quantity = models.IntegerField(validators=[MinValueValidator(1)])

    def __str__(self):
        return '{}: {} {}'.format(self.voucher_number, self.item, self.quantity)


class VoucherReturn(models.Model):
    voucher_number = models.IntegerField()





