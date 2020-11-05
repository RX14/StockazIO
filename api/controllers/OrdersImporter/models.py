from django.db import models
from controllers.categories.models import Category


class Order(models.Model):
    IMPORT_STATE_CHOICES = ((0, "Unknown"), (1, "Fetched"), (2, "Imported"), (99, "Error"))
    date = models.DateTimeField("date")
    # In case of Mouser, the sales order number is different than the web order, and the one to use is the web order
    order_number = models.CharField("order number", max_length=255, unique=True, blank=False)
    status = models.CharField("status of order", max_length=20, default="UNKNOWN")  # UNKNOWN, COMPLETE, etc.
    vendor = models.CharField("vendor", max_length=255, default="unknown")  # mouser, etc. set by the importer system
    import_state = models.IntegerField(
        "import state", default=0, choices=IMPORT_STATE_CHOICES
    )  # 0=unknown, 1=fetched, 2=imported, 99=error


class Item(models.Model):
    vendor_part_number = models.CharField("vendor part number", max_length=255, unique=False, blank=False)
    mfr_part_number = models.CharField("manufacturer part number", max_length=255, unique=False, blank=False)
    manufacturer = models.CharField("manufacturer", max_length=255, unique=False, blank=False)
    description = models.CharField("description", max_length=255, unique=False, blank=False)
    quantity = models.IntegerField("quantity", default=0)
    order = models.ForeignKey(Order, blank=False, null=False, on_delete=models.CASCADE)

    category = models.ForeignKey(Category, blank=True, null=True, on_delete=models.SET_NULL)
    ignore = models.BooleanField("ignore import", default=False)


class CategoryMatcher(models.Model):
    regexp = models.CharField("regexp", max_length=255, blank=False, unique=False)
    category = models.ForeignKey(Category, blank=True, null=True, on_delete=models.CASCADE)
