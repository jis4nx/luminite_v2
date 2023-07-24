from django.http import JsonResponse
from django.template import context
from rest_framework.views import APIView, status
from rest_framework.response import Response
from rest_framework import generics, parsers
from rest_framework import viewsets

from .models.product import Product, ProductItem, Category, OrderItem
from .serializers import (
    ProductItemSerializer,
    ProductSerializer,
    CategorySerializer,
    OrderItemSerializer
)
from shop.models import choices
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


class ProductView(viewsets.ModelViewSet):
    parser_classes = [parsers.FormParser, parsers.MultiPartParser]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductRetrieveView(APIView):
    """
    Get a list of product items of Product Object
    """

    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        if not product:
            return Response(
                {'error': 'Product not found!'},
                status=status.HTTP_404_NOT_FOUND)
        product_serializer = ProductSerializer(product)
        items = product.product_items.all()
        item_serializer = ProductItemSerializer(
            items, many=True, context={'request': request})
        data = {'product': product_serializer.data,
                'items': item_serializer.data}
        return Response(data)


class ShopItemView(APIView):
    def get(self, request):
        products = Product.objects.all()

        data = []
        for product in products:
            item = product.product_items.first()
            product_serializer = ProductSerializer(product)
            item_serializer = ProductItemSerializer(
                item, context={'request': request})
            data.append({
                'product': product_serializer.data,
                'item': item_serializer.data
            })

        return JsonResponse(data, safe=False)


class ShopItemRetrieveView(APIView):
    def get(self, request, pk):
        product_item = generics.get_object_or_404(ProductItem, pk=pk)
        product = product_item.product
        items = product.product_items.select_related('product').all()
        items_serializer = ProductItemSerializer(
            items, many=True, context={'request': request})
        item_serializer = ProductItemSerializer(
            product_item, context={'request': request})
        product_serializer = ProductSerializer(product)
        data = {'product': product_serializer.data,
                'items': items_serializer.data, "item": item_serializer.data}
        return Response(data)


class ProductAttributeView(APIView):
    def get(self, request):
        return Response({
            "colors": [color for color in choices.Colors],
            "size": [size for size in choices.ProductSize]
        })


@extend_schema_view(
    list=extend_schema(
        summary="Lists all Order Items or create one",
        description="Return a list of users all Order Items",
    ),
    retrieve=extend_schema(
        summary="Retrieve Orders or Create one",
        description="Get details of a specific Order or Create One",
    ),
)
class OrderItemView(generics.ListCreateAPIView):
    """Creates Order Items or get all the Order Items"""
    parser_classes = [parsers.FormParser, parsers.MultiPartParser]
    serializer_class = OrderItemSerializer
    queryset = OrderItem.objects.all()
