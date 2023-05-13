from django.db import models


class Colors(models.TextChoices):
    RED = "RED", "Red"
    BLUE = "BLUE", "Blue"
    BLACK = "BLACK", "Black"
    GREEN = "GREEN", "Green"


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
