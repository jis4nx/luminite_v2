from django.db.models import Q, Prefetch, F
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.views import generic
from rest_framework.views import APIView, status
from rest_framework.response import Response
from rest_framework import generics, parsers
from rest_framework import viewsets
from shop.utils import gen_pdf
from django.db.models import OuterRef, Subquery
from django.db import transaction

from shop.models.product import (
    Product,
    ProductItem,
    Category,
    OrderItem,
    Order,
    ProductType,
    Review,
)
from shop.serializers import (
    ProductItemSerializer,
    ProductSerializer,
    CategorySerializer,
    OrderItemSerializer,
    OrderSerializer,
    ReviewSerializer,
    SimpleCategorySerializer,
    UserPaymentSerializer,
    UserProductSerializer,
)
from accounts.serializers import AddressSerializer
from shop.models import choices
from drf_spectacular.utils import extend_schema, extend_schema_view


class Index(APIView):
    """Api endpoints for accessing resources"""

    def get(self, request):
        return redirect(reverse("redoc"))


class CategoryView(generics.ListCreateAPIView):
    """Get a list of categories or create a new category"""

    parser_classes = [parsers.FormParser, parsers.MultiPartParser]
    queryset = Category.objects.filter(parent=None)
    serializer_class = SimpleCategorySerializer


class ProductView(viewsets.ModelViewSet):
    parser_classes = [parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser]
    queryset = Product.objects.all()
    serializer_class = UserProductSerializer


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
        data = {"product": product_serializer.data, "items": item_serializer.data}
        return Response(data)


class ShopItemView(APIView):
    def get(self, request):
        products = Product.objects.all()

        data = []
        for product in products:
            item = product.product_items.first()
            product_serializer = ProductSerializer(product)
            item_serializer = ProductItemSerializer(item, context={"request": request})
            data.append(
                {"product": product_serializer.data, "item": item_serializer.data}
            )

        return JsonResponse(data, safe=False)


class ShopItemRetrieveView(APIView):
    def get(self, request, pk):
        product_item = generics.get_object_or_404(ProductItem, pk=pk)
        product = product_item.product
        items = product.product_items.all()
        attributes = items.get_unique_attributes()
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
            "attributes": attributes,
            "item": item_serializer.data,
            "attributes": attributes,
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

    parser_classes = [parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser]
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
                queryset=OrderItem.objects.select_related("product_item__product"),
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
                Order.objects.select_related("user", "payment", "delivery_address")
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
                "invoice1.html", {"order": data["order"], "products": data["products"]}
            )
            return HttpResponse(pdf, content_type="application/pdf")
        return HttpResponseForbidden(
            "<center>Unauthorized Request, Please Login to view this page</center>"
        )


class OrderItemCreateView(generics.CreateAPIView):
    serializer_class = OrderItemSerializer
    queryset = OrderItem.objects.all()

    def create(self, request, *args, **kwargs):
        mutable_data = request.data.copy()

        items_data = mutable_data.pop("items")
        order_data = mutable_data.get("order")
        order = OrderSerializer(data=order_data)

        if order.is_valid():
            with transaction.atomic():
                order_instance = order.save()
                order_item_data = []
                for item in items_data:
                    item_id = item.get("product_item")
                    product_item = ProductItem.objects.select_related().get(id=item_id)
                    order_item_data.append(
                        dict(
                            item,
                            order=order_instance.id,
                            merchant_id=product_item.product.owner.id,
                        )
                    )

                    product_item.qty_in_stock = F("qty_in_stock") - item.get("qty")
                    product_item.save()

                order_item_serializer = self.get_serializer(
                    data=order_item_data, many=True
                )
                if order_item_serializer.is_valid():
                    order_item_serializer.save()
                    return Response({"msg": "success"}, status=status.HTTP_201_CREATED)

        return Response(order.errors, status=status.HTTP_400_BAD_REQUEST)


class SearchProduct(generics.ListAPIView):
    serializer_class = ProductItemSerializer

    def get_queryset(self):
        product_name = self.request.query_params.get("product", None)
        category_id = self.request.query_params.get("category", None)

        products = Product.objects.prefetch_related("product_items").filter(
            Q(name__icontains=product_name)
            | Q(category=category_id)
            | Q(category__name__icontains=product_name)
        )
        items = (
            ProductItem.objects.prefetch_related("item_reviews__user")
            .select_related(
                "product__category",
                "product_type",
            )
            .filter(product__in=products)
        )
        return items

    def list(self, request):
        serializer_data = self.get_serializer(self.get_queryset(), many=True).data
        list_id = self.get_queryset().values_list("id", flat=True)
        data = dict(items=serializer_data, list_id=list_id)
        return Response(data)


class ProductItemFilter(APIView):
    def post(self, request):
        attr_data = {k: v for k, v in request.data.get("attributes").items() if v}
        list_id = request.data.get("list_id")
        color_data = request.data.get("colors")
        query = Q()
        color_query = Q(product_color__in=color_data)
        price = request.data.get("price")
        attr_query = Q(**{f"attributes__{k}__in": v for k, v in attr_data.items()})
        price_query = Q(price__gte=price.get("min"), price__lte=price.get("max"))
        if color_data:
            query &= color_query
        if attr_data:
            query &= attr_query
        if price:
            query &= price_query
        filtered_items = ProductItem.objects.filter(query, id__in=list_id)
        print(query)
        print(list_id)
        print(filtered_items)
        items = ProductItemSerializer(
            filtered_items, many=True, context={"request": request}
        ).data
        if request.data:
            return Response(items)
        return Response([])


class UserReview(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()
    parser_classes = [parsers.JSONParser, parsers.FormParser]


class RetrieveUserReview(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()
