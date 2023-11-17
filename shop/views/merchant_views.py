from rest_framework.views import APIView, Response, status
from rest_framework import generics, parsers
from django.db.models import Q, Prefetch
from shop.models.product import OrderItem, Product, ProductType
from rest_framework.pagination import LimitOffsetPagination
from collections import defaultdict
from shop.serializers import (
    MerchantOrderItemSerializer,
    MerchantProductItemSerializer,
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


class MerchantProductFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(
        field_name="category__name", lookup_expr="icontains"
    )
    name = django_filters.CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = Product
        fields = ["category", "name"]


class CreateItemView(generics.CreateAPIView):
    serializer_class = MerchantProductItemSerializer
    queryset = ProductItem.objects.all()
    parser_classes = [parsers.JSONParser, parsers.MultiPartParser]


class GetItemView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MerchantProductItemSerializer
    queryset = ProductItem.objects.all()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.serializer_class(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)


class MerchantProducts(generics.ListAPIView):
    serializer_class = UserProductSerializer
    pagination_class = LimitOffsetPagination
    filterset_class = MerchantProductFilter
    ordering_fields = ["base_price"]

    def get_queryset(self):
        product = Product.objects.select_related("category", "category__parent").filter(
            owner__id=self.request.user.id
        )
        return product


class GetMerchantProduct(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserProductSerializer

    def get_queryset(self):
        product = Product.objects.filter(owner=self.request.user.id)
        return product


class ListProductItems(generics.ListAPIView):
    serializer_class = ProductItemSerializer
    pagination_class = LimitOffsetPagination
    ordering_fields = ["qty_in_stock"]

    def get_queryset(self):
        attr_params = self.request.query_params
        price = self.request.query_params.get("price", None)
        qty = self.request.query_params.get("qty", None)

        product_id = self.kwargs["pk"]
        items = (
            ProductItem.objects.select_related("product")
            .filter(product=product_id)
            .attribute_filter(attr_params, price=price, qty=qty)
        )
        return items

    # Getting all the attributes unique keys with their respective values

    def list(self, request, *args, **kwargs):
        qs = self.get_queryset()
        attributes = qs.get_unique_attributes()
        serializer = self.get_serializer(qs, many=True)
        resp = {
            "attributes": attributes,
            "items": serializer.data,
        }
        return Response(resp)


class GetProductTypes(generics.ListAPIView):
    serializer_class = ProductTypeSerializer
    queryset = ProductType.objects.all()


# class MerchantProductItemFilter(django_filters.FilterSet):
#     name = django_filters.CharFilter(
#         field_name="product__name", lookup_expr="icontains"
#     )
#
#     class Meta:
#         model = ProductItem
#         fields = ["name", "qty_in_stock", "price"]
#
#
# class ListProductItems(generics.ListAPIView):
#     serializer_class = ProductItemSerializer
#     pagination_class = LimitOffsetPagination
#     filterset_class = MerchantProductItemFilter
#     ordering_fields = ["qty_in_stock", "price"]
#
#     def get_queryset(self):
#         owner_id = self.request.user.id
#         products = ProductItem.objects.select_related("product").filter(
#             product__owner=owner_id
#         )
#         return products
