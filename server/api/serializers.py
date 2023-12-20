import uuid
import datetime 

from rest_framework import serializers
from django.utils import timezone
from api.models import Restaurent, Voucher, Customer, CustomerVoucher, PurchaseHistory


class VoucherSerialzier(serializers.Serializer):
    
    name = serializers.CharField(max_length=250)
    validity = serializers.DateTimeField()
    description = serializers.CharField(max_length=250)
    purchase_value = serializers.IntegerField()
    credit_value = serializers.IntegerField()
    restaurent =  serializers.PrimaryKeyRelatedField(queryset=Restaurent.objects.all())
    voucher_count = serializers.IntegerField()

    def validate_purchase_value(self, value):
        if value <= 10:
            raise serializers.ValidationError("Minimum Buy value should be greater than 10")
        return value
    
    def validate_validity(self, value):
        
        if value < timezone.now():
            raise serializers.ValidationError("Validity date should be greater than current date")
        return value
    
    def validate_credit_value(self, value):
        if value > 5000:
            raise serializers.ValidationError("The “get” amount cannot exceed $5000")
        return value
    
    def validate(self, data):
        print(data, "data")
        if data['credit_value'] < data['purchase_value']:
            raise serializers.ValidationError("Credit value should be greater than purchase value")
        elif data['credit_value'] > data['purchase_value'] * 2:
            raise serializers.ValidationError("Credit value should not be greater than double of purchase value")
        return data 
    
    def create(self, validated_data):
        voucher_count = validated_data.pop('voucher_count')
        for i in range(voucher_count):
            validated_data["voucher_code"] = uuid.uuid4()
            Voucher.objects.create(**validated_data)
        return True


class PurchaseSerializer(serializers.Serializer):

    customer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all())
    restaurent = serializers.PrimaryKeyRelatedField(queryset=Restaurent.objects.all())
    voucher_value = serializers.IntegerField()

    def validate(self, data):
        print("coming")
        voucher = Voucher.objects.filter(restaurent=data['restaurent'], purchase_value=data['voucher_value'], status='available')
        if not voucher.exists():
            raise serializers.ValidationError("Voucher value not available for selected restaurent")

        return data
    
    def create(self, validated_data):
        print(validated_data)
        voucher_list = Voucher.objects.filter(restaurent=validated_data['restaurent'], 
                                         status='available',
                                         purchase_value=validated_data['voucher_value']
                                         )
        voucher = voucher_list[0]
        CustomerVoucher.objects.create(
            customer=validated_data['customer'],
            voucher=voucher
        )
        voucher.status = 'sold'
        voucher.save()
        customer = validated_data['customer']
        customer.wallet += voucher.credit_value
        customer.save()
        return True



class RedeemSerializer(serializers.Serializer):

    customer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all())
    restaurent = serializers.PrimaryKeyRelatedField(queryset=Restaurent.objects.all())
    coupon_code = serializers.CharField()
    bill_amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    
    def validate(self, data):
        try:
            customer_voucher = CustomerVoucher.objects.get(customer=data['customer'],
                                    voucher__restaurent=data['restaurent'],
                                      voucher__voucher_code=data['coupon_code'],
                                        is_used=False)
            
        except CustomerVoucher.DoesNotExist:
            raise serializers.ValidationError("Coupon not valid")
        
        else:
            if data['bill_amount'] < customer_voucher.voucher.credit_value:
                raise serializers.ValidationError("Bill Amount should be greater than voucher value. You can't use voucher")
        return data

    def create(self, validated_data):

        customer_voucher = CustomerVoucher.objects.get(customer=validated_data['customer'],
                                    voucher__restaurent=validated_data['restaurent'],
                                      voucher__voucher_code=validated_data['coupon_code'],
                                        is_used=False)
        balance_amount = validated_data["bill_amount"] - customer_voucher.voucher.credit_value
        ph = PurchaseHistory.objects.create(
            customer=validated_data['customer'],
            restaurent=validated_data['restaurent'],
            bill_amount=validated_data['bill_amount'],
            used_voucher=customer_voucher,
            paid_by_cash=balance_amount,
            used_voucher_value=customer_voucher.voucher.credit_value
        )
        customer = validated_data['customer']
        customer.wallet -= customer_voucher.voucher.credit_value
        customer.save()
        customer_voucher.is_used = True
        customer_voucher.save()
        return True

class GetVoucherSerialzier(serializers.ModelSerializer):
    class Meta:
        model = Voucher
        fields = "__all__"
        
class CustomerVoucherSerializer(serializers.ModelSerializer):
    voucher = GetVoucherSerialzier()
    class Meta:
        model = CustomerVoucher
        fields = ("voucher", "is_used")
