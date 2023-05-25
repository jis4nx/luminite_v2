from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, parsers
from .models.product import Product, ProductItem, Category, OrderItem
from .serializers import (
    ProductItemSerializer,
    ProductSerializer,
    CategorySerializer,
    OrderItemSerializer
)
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, extend_schema_view


class Index(APIView):
    """Api endpoints for accessing resources"""

    def get(self, request):
        navs = ["Products: /shop/products/"]
        return Response(navs)


class CategoryView(generics.ListCreateAPIView):
    """Get a list of categories or create a new category"""

    parser_classes = [parsers.FormParser, parsers.MultiPartParser]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    @extend_schema(
        summary="lists category or create one",
        responses={200: CategorySerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(self, request, *args, **kwargs)


class ProductView(generics.ListCreateAPIView):
    parser_classes = [parsers.FormParser, parsers.MultiPartParser]
    serializer_class = ProductSerializer
    queryset = Product.objects.all()


class ProductItemView(generics.ListCreateAPIView):
    """
    Get a list of product items or create a new product item
    """
    parser_classes = [parsers.FormParser, parsers.MultiPartParser]
    serializer_class = ProductItemSerializer
    queryset = ProductItem.objects.all()

    @extend_schema(
        summary="lists product items or create one",
        responses={200: ProductItemSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        super().get(self, request, *args, **kwargs)


@extend_schema_view(
    list=extend_schema(
        summary="Lists all Order Items or create one",
        description="Return a list of users all Order Items",
    ),
    retrieve=extend_schema(
        summary="Retrieve user",
        description="Get details of a specific user",
    ),
)
class OrderItemView(ModelViewSet):
    """Creates Order Items or get all the Order Items"""
    parser_classes = [parsers.FormParser, parsers.MultiPartParser]
    serializer_class = OrderItemSerializer
    queryset = OrderItem.objects.all()
