from django.db import models
from enum import Enum


# class Colors(models.TextChoices):
#     RED = "RED", "Red"
#     BLUE = "BLUE", "Blue"
#     BLACK = "BLACK", "Black"
#     GREEN = "GREEN", "Green"


class ColorChoices(Enum):
    WHITE = ("#FFFFFF", "White")
    BLACK = ("#000000", "Black")
    RED = ("#FF0000", "Red")
    MAROON = ("#800000", "Maroon")
    CRIMSON = ("#DC143C", "Crimson")
    YELLOW = ("#FFFF00", "Yellow")
    GREEN = ("#008000", "Green")
    LIME = ("#00FF00", "Lime")
    NAVY = ("#000080", "Navy")
    BLUE = ("#0000FF", "Blue")
    PURPLE = ("#800080", "Purple")
    PINK = ("#FFC0CB", "Pink")
    DEEPPINK = ("#FF1493", "Deep Pink")

    @classmethod
    def choices(cls):
        return [(item.value[1], item.value[1]) for item in cls]

    @classmethod
    def color_code(cls, name):
        hex_map = {item.value[1]: item.value[0] for item in cls}
        return hex_map.get(name)


class Status(models.TextChoices):
    PENDING = "PD", "Pending"
    CONFIRMED = "CD", "Confirmed"
    DELIVERED = "DL", "Delivered"


class DeliveryMethods(models.TextChoices):
    PTH = "PTH", "Pathao"
    REDX = "REDX", "REDX"
    FEDX = "FEDX", "FedEX"
    DHL = "DHL", "DHL"


class ProductSize(models.TextChoices):
    S = "S", "S"
    M = "M", "M"
    X = "X", "X"
    XL = "XL", "XL"
    XLL = "XLL", "XLL"


class PaymentMethod(models.TextChoices):
    BKS = "BKASH", "Bkash"
    NGD = "NAGAD", "Nagad"
    COD = "COD", "Cash On Deliver"
