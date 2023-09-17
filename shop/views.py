from django.db.models import Q, Prefetch
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from rest_framework.views import APIView, status
from rest_framework.response import Response
from rest_framework import generics, parsers
from rest_framework import viewsets
from shop.utils import gen_pdf
from django.db.models import OuterRef, Subquery
import django_filters
from django_filters.rest_framework import DjangoFilterBackend

from .models.product import Product, ProductItem, Category, OrderItem, Order, ProductType
from .serializers import (
    ProductItemSerializer,
    ProductSerializer,
    CategorySerializer,
    OrderItemSerializer,
    OrderSerializer,
    UserPaymentSerializer,
)
from accounts.serializers import AddressSerializer
from shop.models import choices
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


class CreateItemView(APIView):
    def post(self, request):
        item_data = self.request.data
        product_attributes = item_data.get('attributes')
        product_type = item_data.get('product_type')
        product_id = item_data.get('product')
        product = generics.get_object_or_404(Product, pk=product_id)
        product_type = item_data.get('product_type')
        getType = generics.get_object_or_404(
            ProductType, product_type=product_type)

        if all(k in getType.attributes for k in product_attributes):
            ProductItem.objects.create(
                product=product, qty_in_stock=item_data.get('qty'),
                price=item_data.get('price'), attributes=product_attributes)
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


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
                {"error": "Product not found!"}, status=status.HTTP_404_NOT_FOUND
            )
        product_serializer = ProductSerializer(product)
        items = product.product_items.all()
        item_serializer = ProductItemSerializer(
            items, many=True, context={"request": request}
        )
        data = {"product": product_serializer.data,
                "items": item_serializer.data}
        return Response(data)


class ShopItemView(APIView):
    def get(self, request):
        products = Product.objects.all()

        data = []
        for product in products:
            item = product.product_items.first()
            product_serializer = ProductSerializer(product)
            item_serializer = ProductItemSerializer(
                item, context={"request": request})
            data.append(
                {"product": product_serializer.data, "item": item_serializer.data}
            )

        return JsonResponse(data, safe=False)


class ShopItemRetrieveView(APIView):
    def get(self, request, pk):
        product_item = generics.get_object_or_404(ProductItem, pk=pk)
        product = product_item.product
        items = product.product_items.select_related("product").all()
        items_serializer = ProductItemSerializer(
            items, many=True, context={"request": request}
        )
        item_serializer = ProductItemSerializer(
            product_item, context={"request": request}
        )
        product_serializer = ProductSerializer(product)
        data = {
            "product": product_serializer.data,
            "items": items_serializer.data,
            "item": item_serializer.data,
        }
        return Response(data)


class ProductAttributeView(APIView):
    def get(self, request):
        return Response(
            {
                "colors": [color for color in choices.Colors],
                "size": [size for size in choices.ProductSize],
            }
        )


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

    parser_classes = [parsers.FormParser,
                      parsers.MultiPartParser, parsers.JSONParser]
    serializer_class = OrderItemSerializer
    queryset = OrderItem.objects.all()


class GetUserOrders(APIView):
    def get(self, request):
        user = request.user.userprofile

        user_orders = user.order_set.select_related(
            "payment", "delivery_address"
        ).prefetch_related(
            Prefetch(
                "items",
                queryset=OrderItem.objects.select_related(
                    "product_item__product"),
            )
        )

        order_data = [
            {
                "order": {
                    "id": order.id,
                    "deliveryAddress": str(order.delivery_address),
                    "deliveryMethod": order.delivery_method,
                    "orderDate": order.created_at,
                    "status": order.status,
                    "totalPrice": order.get_total_cost(),
                    "payment": UserPaymentSerializer(order.payment).data,
                },
                "products": [
                    {
                        "id": item.product_item.id,
                        "name": item.product_item.product.name,
                        "image": item.product_item.image.url,
                        "price": item.price,
                        "qty": item.qty,
                    }
                    for item in order.items.all()
                ],
            }
            for order in user_orders
        ]

        return Response(order_data)


class GetInvoicePDF(APIView):
    def get(self, request, orderId):
        if not self.request.user.is_anonymous:
            orderObj = (
                Order.objects.select_related(
                    "user", "payment", "delivery_address")
                .prefetch_related(
                    Prefetch(
                        "items",
                        queryset=OrderItem.objects.select_related(
                            "product_item__product"
                        ),
                    )
                )
                .get(user=request.user.userprofile, id=orderId)
            )

            data = {
                "order": {
                    "id": orderObj.id,
                    "payment": UserPaymentSerializer(orderObj.payment).data,
                    "deliveryAddress": AddressSerializer(
                        orderObj.delivery_address
                    ).data,
                    "deliveryMethod": orderObj.delivery_method,
                    "orderDate": orderObj.created_at,
                    "totalPrice": orderObj.get_total_cost(),
                    "user": orderObj.user.user.email,
                },
                "products": [
                    {
                        "id": item.product_item.id,
                        "name": item.product_item.product.name,
                        "image": item.product_item.image.url,
                        "price": item.price,
                        "qty": item.qty,
                        "subTotal": item.qty * item.price,
                    }
                    for item in orderObj.items.all()
                ],
            }

            pdf = gen_pdf(
                "invoice1.html", {
                    "order": data["order"], "products": data["products"]}
            )
            return HttpResponse(pdf, content_type="application/pdf")
        return HttpResponseForbidden(
            "<center>Unauthorized Request, Please Login to view this page</center>"
        )


class OrderItemCreateView(generics.CreateAPIView):
    serializer_class = OrderItemSerializer
    queryset = OrderItem.objects.all()

    def create(self, request, *args, **kwargs):
        items_data = request.data.pop("items")
        order_data = request.data.get("order")
        order = OrderSerializer(data=order_data)

        if order.is_valid():
            order_instance = order.save()
            order_item_data = [
                dict(item, order=order_instance.id) for item in items_data
            ]
            order_item_serializer = self.get_serializer(
                data=order_item_data, many=True)
            if order_item_serializer.is_valid():
                order_item_serializer.save()
                return Response({"msg": "success"}, status=status.HTTP_201_CREATED)

        return Response(order.errors, status=status.HTTP_400_BAD_REQUEST)


class SearchProduct(APIView):
    def get(self, request):
        product_name = self.request.query_params.get("product", None)
        category_id = self.request.query_params.get("category", None)
        if product_name or category_id:

            product_objs = self.filter_products_with_items(
                product=product_name, category=category_id)
            res = self.serialize_products(product_objs)
            return Response(res)

    def filter_products_with_items(self, product=None, category=None):
        first_product_item = ProductItem.objects.filter(
            product=OuterRef("pk"), qty_in_stock__gt=1
        ).order_by("id")

        query = Q()

        if product is not None:
            query |= Q(name__icontains=product)

        if category is not None:
            query |= Q(category=category)

        product_objs = Product.objects.filter(query).annotate(
            first_item_id=Subquery(first_product_item.values("id")[:1])
        )

        return product_objs

    def serialize_products(self, product_objs):
        res = [
            {
                "name": product.name,
                "item": ProductItemSerializer(
                    product.product_items.get(id=product.first_item_id)
                ).data,
                "items": ProductItemSerializer(product.product_items, many=True).data
            }
            for product in product_objs
        ]
        return res


class ProductItemFilter(APIView):
    def post(self, request):
        attr_data = {k: v for k, v in request.data.get(
            'attributes').items() if v}
        price = request.data.get('price')
        attr_query = Q(**{f"attributes__{k}__in": v for k,
                          v in attr_data.items()})
        price_query = Q(price__gte=price.get('min'),
                        price__lte=price.get('max'))
        filtered_items = ProductItem.objects.filter(attr_query, price_query)
        items = ProductItemSerializer(filtered_items, many=True).data
        if request.data:
            return Response(items)
        return Response([])
