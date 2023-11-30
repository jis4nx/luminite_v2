from django.db.models.query import Prefetch
from django.http import HttpResponse
from django.template.loader import get_template
from weasyprint import HTML
from accounts.serializers import AddressSerializer

from shop.models.product import Order, OrderItem
from shop.serializers import UserPaymentSerializer
from django.template.loader import render_to_string


def gen_pdf(template_source, context_dict={}):
    template = get_template(template_source)
    html_content = template.render(context_dict)
    html = HTML(string=html_content)
    pdf = html.write_pdf()

    response = HttpResponse(pdf, content_type="application/pdf")
    response["Content-Disposition"] = 'filename="invoice.pdf"'
    return response


def generate_invoice(user_profile, order_id, html=False):
    orderObj = (
        Order.objects.select_related("user", "payment", "delivery_address")
        .prefetch_related(
            Prefetch(
                "items",
                queryset=OrderItem.objects.select_related("product_item__product"),
            )
        )
        .get(user=user_profile, id=order_id)
    )

    data = {
        "order": {
            "id": orderObj.id,
            "payment": UserPaymentSerializer(orderObj.payment).data,
            "deliveryAddress": AddressSerializer(orderObj.delivery_address).data,
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
    context = {"order": data["order"], "products": data["products"]}
    if html:
        html_string = render_to_string("order-summary.html", context)
        return html_string

    pdf = gen_pdf("invoice1.html", context)
    return pdf
