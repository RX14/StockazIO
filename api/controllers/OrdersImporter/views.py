from rest_framework.viewsets import ModelViewSet
from rest_framework import views
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .serializers import OrderSerializer, CategoryMatcherSerializer, OrderCreateSerializer
from .models import CategoryMatcher, Order
from controllers.categories.models import Category
from controllers.part.models import Part
from controllers.manufacturer.models import PartManufacturer
from controllers.distributor.models import DistributorSku
from .utils import rematch_orders


class OrderViewSet(ModelViewSet):
    anonymous_policy = False
    required_scope = {
        "retrieve": "read",
        "create": "write",
        "destroy": "write",
        "update": "write",
        "partial_update": "write",
        "list": "read",
    }
    ordering_fields = ["date", "order_number", "status", "vendor", "import_state"]
    ordering = ["date"]

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return OrderSerializer
        else:
            return OrderCreateSerializer

    def get_queryset(self):
        queryset = Order.objects.all()
        return queryset


class CategoryMatcherViewSet(ModelViewSet):
    anonymous_policy = False
    required_scope = {
        "retrieve": "read",
        "create": "write",
        "destroy": "write",
        "update": "write",
        "partial_update": "write",
        "list": "read",
    }
    serializer_class = CategoryMatcherSerializer

    def get_queryset(self):
        queryset = CategoryMatcher.objects.all()
        return queryset


class CategoryMatcherBatchUpdater(views.APIView):
    required_scope = "parts"
    anonymous_policy = False

    def patch(self, req):
        # Missing elements will be created
        new_items = []
        if len(req.data) <= 0:
            return Response({"detail": "Not found."}, 404)
        for item in req.data:
            if "id" in item:
                # Update
                db_item = CategoryMatcher.objects.get(id=item["id"])
                if db_item:
                    db_item.regexp = item["regexp"]
                    category = Category.objects.get(id=item["category"])
                    if not category:
                        continue
                    db_item.category = category
                    db_item.save()
            else:
                # Create
                category = Category.objects.get(id=item["category"])
                if not category:
                    continue
                db_item = CategoryMatcher(regexp=item["regexp"], category=category)
                db_item.save()
            new_items.append(db_item)
        serializer = CategoryMatcherSerializer(new_items, many=True)
        return Response(serializer.data, status=200)


class CategoryMatcherBatchRematcher(views.APIView):
    required_scope = "parts"
    anonymous_policy = False

    def get(self, req):
        # fetch orders
        orders = Order.objects.all().filter(import_state=1).prefetch_related("items")
        if not orders:
            return Response({"details": "ok"}, 200)

        # rematch
        rematch_orders(orders)

        return Response({"detail": "done"})


class OrderImporterToInventory(views.APIView):
    required_scope = "parts"
    anonymous_policy = False

    def post(self, req):
        if "id" not in req.data:
            return Response({"detail": "id is missing"}, 503)

        order = get_object_or_404(Order.objects.prefetch_related("items"), id=req.data["id"])

        if order.import_state != 1:  # refuse if import state isn't 1/fetched
            return Response({"detail": f"order import state {order.import_state} isn't valid for importing"})

        for item in order.items.all():
            if item.ignore:
                continue

            # Try to see if we already have an item in db
            try:
                part = Part.objects.get(name=item.mfr_part_number)
            except Part.DoesNotExist:
                part = None

            if part:
                # TODO/FIXME add a manufacturer sku if not; add a distributor sku if not
                part.stock_qty += item.quantity
                if not part.category:
                    part.category = item.category
                if not part.description:
                    part.description = item.description
                part.save()
            else:
                part = Part(
                    name=item.mfr_part_number,
                    stock_qty=item.quantity,
                    description=item.description,
                    category=item.category,
                )
                part.save()

                manuf_sku = PartManufacturer(sku=item.mfr_part_number, manufacturer=item.manufacturer_db, part=part)
                manuf_sku.save()
                part.manufacturers_sku.add(manuf_sku)

                distri_sku = DistributorSku(sku=item.vendor_part_number, distributor=order.vendor_db, part=part)
                distri_sku.save()
                part.distributors_sku.add(distri_sku)

                # TODO/FIXME add a manufacturer sku; add a distributor sku
                part.save()
        # finally, set import_state to 2

        return Response({"detail": "done"})
