from django.db import models
from django.db.models import Q


class ProductItemQuerySet(models.QuerySet):
    def attribute_filter(self, attributes, price=None, qty=None):
        query = Q()
        for k, v in attributes.lists():
            if k not in ["qty", "price"]:
                query &= Q(
                    **{f"attributes__{k}__in": [v] if type(v) is not list else v}
                )
        if price:
            query &= Q(price=price)
        if qty:
            query &= Q(qty_in_stock__lte=qty)
        items = self.filter(query)
        return items


class ProductItemManager(models.Manager):
    def get_queryset(self):
        return ProductItemQuerySet(self.model, using=self._db)

    def attribute_filter(self, attributes, price=None, qty=None):
        return self.get_queryset().attribute_filter(attributes, price=price, qty=qty)
