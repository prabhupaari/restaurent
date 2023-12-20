from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.serializers import VoucherSerialzier, PurchaseSerializer, RedeemSerializer, CustomerVoucherSerializer
from api.models import CustomerVoucher


class Vouchers(APIView):

    def post(self, request):
        data = self.request.data
        serializer = VoucherSerialzier(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"Voucher Created Successfully"})
        else:
            return Response({"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class Purchase(APIView):

    def post(self, request):
        data = self.request.data
        serializer = PurchaseSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"Voucher Created Successfully"})
        else:
            return Response({"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class Redeem(APIView):

    def post(self, request):
        data = self.request.data
        serializer = RedeemSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"Redeemed Successfully"})
        else:
            return Response({"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class CustomerVoucherAPI(APIView):
    def post(self, request):
        data = request.data
        customer = data.get('customer')
        if not customer:
            return Response({"message": "customer data mandatory"}, status=status.HTTP_400_BAD_REQUEST)
        customer_voucher = CustomerVoucher.objects.filter(customer=customer)
        if customer_voucher.exists():
            serializer = CustomerVoucherSerializer(customer_voucher, many=True)
            return Response({"data":serializer.data})
        else:
            return Response({"message": "No data available"}, status=status.HTTP_404_NOT_FOUND)