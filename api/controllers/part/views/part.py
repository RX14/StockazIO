from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from controllers.part.models import Part
from controllers.part.forms import PartForm
from controllers.categories.models import Category
from controllers.distributor.models import DistributorSku
from controllers.distributor.forms import DistributorSkuForm

from django.forms.models import inlineformset_factory
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from django.db import transaction
from controllers.distributor.forms import DistributorSkuFormSet
from django.utils.decorators import method_decorator


@login_required
def part_list(request, category=None, template_name="parts/part_list.html"):
    sort = request.GET.get("sort", "name")
    page = request.GET.get("page", 1)
    q = request.GET.get("q", None)
    ctx = {}

    if sort == "name":
        ctx["sort_arg"] = "-name"
        ctx["sort_by"] = "name"
    elif sort == "-name":
        ctx["sort_arg"] = "name"
        ctx["sort_by"] = "-name"

    if category:
        cat = get_object_or_404(Category, id=category)
        base_queryset = Part.objects.prefetch_related("storage", "footprint").filter(category=cat)
    else:
        base_queryset = Part.objects.prefetch_related("storage", "footprint")

    if q:
        base_queryset = base_queryset.filter(name__icontains=q)

    ctx["object_list"] = base_queryset.order_by(ctx["sort_by"])
    paginator = Paginator(ctx["object_list"], settings.PAGINATION["PARTS"])
    ctx["paginator"] = paginator.page(page)
    ctx["page"] = page
    if category:
        ctx["category"] = cat
        ctx["category_path"] = cat.__str__().split("->")

    return render(request, template_name, ctx)


@login_required
def part_create(request, template_name="parts/part_create.html"):
    form = PartForm(request.POST or None)
    distributor_sku_inline_formset = inlineformset_factory(
        Part, DistributorSku, can_delete=True, extra=1, form=DistributorSkuForm
    )

    if request.method == "POST":
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            form.save_m2m()
            formset = distributor_sku_inline_formset(request.POST, instance=obj)
            if formset.is_valid():
                formset.save()
                messages.success(request, "Part successfully created.")
                return redirect("part_list")
    return render(
        request, template_name, {"form": form, "distributor_sku_inline_formset": distributor_sku_inline_formset}
    )


@login_required
def part_update(request, pk, template_name="parts/part_update.html"):
    part = get_object_or_404(Part, pk=pk)
    form = PartForm(request.POST or None, instance=part)
    if form.is_valid():
        form.save()
        messages.success(request, "Part successfully updated.")
        return redirect("part_list")
    return render(request, template_name, {"form": form, "object": part})


class PartCreate(CreateView):
    model = Part
    template_name = "parts/part_create.html"
    form_class = PartForm
    success_url = None

    def get_context_data(self, **kwargs):
        data = super(PartCreate, self).get_context_data(**kwargs)
        if self.request.POST:
            data["distributors_sku"] = DistributorSkuFormSet(self.request.POST)
        else:
            data["distributors_sku"] = DistributorSkuFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        distributors_sku = context["distributors_sku"]
        with transaction.atomic():
            self.object = form.save(commit=False)
            self.object.save()
            form.save_m2m()
            if distributors_sku.is_valid():
                distributors_sku.instance = self.object
                distributors_sku.save()
        return super(PartCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy("part_list")

    @method_decorator(login_required())
    def dispatch(self, *args, **kwargs):
        return super(PartCreate, self).dispatch(*args, **kwargs)


class PartUpdate(UpdateView):
    model = Part
    template_name = "parts/part_update.html"
    form_class = PartForm
    success_url = None

    def get_context_data(self, **kwargs):
        data = super(PartUpdate, self).get_context_data(**kwargs)
        if self.request.POST:
            data["distributors_sku"] = DistributorSkuFormSet(self.request.POST, instance=self.object)
        else:
            data["distributors_sku"] = DistributorSkuFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        distributors_sku = context["distributors_sku"]
        with transaction.atomic():
            form.instance.created_by = self.request.user
            self.object = form.save()
            if distributors_sku.is_valid():
                distributors_sku.instance = self.object
                distributors_sku.save()
        return super(PartUpdate, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy("part_list")

    @method_decorator(login_required())
    def dispatch(self, *args, **kwargs):
        return super(PartUpdate, self).dispatch(*args, **kwargs)
