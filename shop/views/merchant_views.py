from rest_framework.views import APIView, Response, status
from rest_framework import generics
from django.db.models import Q, Prefetch
from shop.models.product import OrderItem, Product, ProductType
from rest_framework.pagination import LimitOffsetPagination
from shop.serializers import (
    MerchantOrderItemSerializer,
    ProductItemSerializer,
    ProductTypeSerializer,
    UserProductSerializer,
)
from shop.models.product import ProductItem, Order
import django_filters


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


class GetMerchantProducts(generics.ListAPIView):
    serializer_class = UserProductSerializer

    def get_queryset(self):
        product = Product.objects.filter(owner=self.request.user.id)
        return product


class GetProductTypes(generics.ListAPIView):
    serializer_class = ProductTypeSerializer
    queryset = ProductType.objects.all()


class MerchantProductItemFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        field_name="product__name", lookup_expr="icontains"
    )

    class Meta:
        model = ProductItem
        fields = ["name", "qty_in_stock", "price"]


class ListProductItems(generics.ListAPIView):
    serializer_class = ProductItemSerializer
    pagination_class = LimitOffsetPagination
    filterset_class = MerchantProductItemFilter
    ordering_fields = ["qty_in_stock", "price"]

    def get_queryset(self):
        owner_id = self.request.user.id
        products = ProductItem.objects.select_related("product").filter(
            product__owner=owner_id
        )
        return products
