from django.db import models

# Create your models here.
VOUCHER_STATUS = (
    ('sold', 'Sold'),
    ('expired', 'Expired'),
    ('available', 'Available')
)
class Restaurent(models.Model):
    name = models.CharField(max_length=250)
    branch_name = models.CharField(max_length=250, null=True, blank=True)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self) -> str:
        return self.name

class Voucher(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=255)
    validity = models.DateTimeField()
    created_at = models.DateTimeField(auto_now=True)
    purchase_value = models.IntegerField(default=10)
    credit_value = models.IntegerField(default=10)
    restaurent = models.ForeignKey(Restaurent, on_delete=models.SET_NULL, null=True, blank=True)
    voucher_code = models.CharField(max_length=30)
    status = models.CharField(max_length=10, choices=VOUCHER_STATUS, default='available')

    def __str__(self) -> str:
        return self.voucher_code


class Customer(models.Model):
    name = models.CharField(max_length=250)
    wallet = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name

class CustomerVoucher(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    voucher = models.ForeignKey(Voucher, on_delete=models.CASCADE)
    is_used = models.BooleanField(default=False)


class PurchaseHistory(models.Model):
    restaurent = models.ForeignKey(Restaurent, on_delete=models.SET_NULL, null=True, blank=True)
    bill_amount = models.DecimalField(max_digits=10, decimal_places=2)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    used_voucher = models.ForeignKey(CustomerVoucher, on_delete=models.SET_NULL, null=True, blank=True)
    paid_amount = models.IntegerField(default=0)
    paid_by_cash = models.IntegerField(default=0)
    used_voucher_value = models.IntegerField(default=0)