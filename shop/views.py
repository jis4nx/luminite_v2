from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, parsers
from .models.product import Product, ProductItem, Category, ShopCart
from .serializers import ProductItemSerializer, ProductSerializer, CategorySerializer, CartSerializer


class Index(APIView):
    def get(self, request):
        navs = [
            "Products: /shop/products/"
        ]
        return Response(navs)


class CategoryView(generics.ListCreateAPIView):
    parser_classes = [parsers.FormParser, parsers.MultiPartParser]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class ProductView(generics.ListCreateAPIView):
    parser_classes = [parsers.FormParser, parsers.MultiPartParser]
    serializer_class = ProductSerializer
    queryset = Product.objects.all()


class ProductItemView(generics.ListCreateAPIView):
    parser_classes = [parsers.FormParser, parsers.MultiPartParser]
    serializer_class = ProductItemSerializer
    queryset = ProductItem.objects.all()


class ShopCartView(generics.ListCreateAPIView):
    parser_classes = [parsers.FormParser, parsers.MultiPartParser]
    serializer_class = CartSerializer
    queryset = ShopCart.objects.all()
