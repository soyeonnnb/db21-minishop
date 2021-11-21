from django.shortcuts import render
from django.views.generic import ListView, DetailView
from . import models

# Create your views here.
class HomeView(ListView):

    """HomeView Definition"""

    model = models.Product
    paginate_by = 12
    paginate_orphans = 4
    ordering = "created_at"
    context_object_name = "products"


class ProductDetailView(DetailView):

    """Product Detail View Definition"""

    model = models.Product
