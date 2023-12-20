from django.contrib import admin

from api.models import Restaurent, Voucher, Customer, PurchaseHistory, CustomerVoucher
# Register your models here.
admin.site.register(Restaurent)
admin.site.register(Voucher)
admin.site.register(Customer)
admin.site.register(PurchaseHistory)
admin.site.register(CustomerVoucher)