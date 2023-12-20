from django.urls import path
from api.views import Vouchers, Purchase, Redeem, CustomerVoucherAPI


urlpatterns = [
    path('voucher/', Vouchers.as_view(), name="vouchers"),
    path('purchase/', Purchase.as_view(), name="purchase"),
    path('redeem/', Redeem.as_view(), name="redeem"),
    path('customer_voucher/', CustomerVoucherAPI.as_view(), name="customer_voucher")
]
