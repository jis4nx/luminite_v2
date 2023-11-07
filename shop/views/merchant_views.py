from rest_framework.views import APIView, Response, status
from rest_framework import generics
from django.db.models import Q, Prefetch
from shop.models.product import OrderItem
from rest_framework.pagination import LimitOffsetPagination
from shop.serializers import MerchantOrderItemSerializer
from shop.models.product import ProductItem, Order


class ListOrders(generics.ListAPIView):
    pagination_class = LimitOffsetPagination
    serializer_class = MerchantOrderItemSerializer

    def get_queryset(self):
        if self.request.user.type == "SELLER":
            merchant_id = self.request.user.id
            order_items = OrderItem.objects.filter(
                merchant_id=merchant_id
            ).prefetch_related(
                Prefetch("product_item", queryset=ProductItem.objects.all()),
                Prefetch(
                    "order", queryset=Order.objects.select_related("delivery_address")
                ),
            )

            return order_items
        return Response(status=status.HTTP_403_FORBIDDEN)
