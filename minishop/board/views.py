from django.shortcuts import render
from django.views.generic import ListView, DetailView

from . import models

# Create your views here.
class FAQListView(ListView):

    """FAQListView Definition"""

    model = models.FAQPost
    paginate_by = 12
    paginate_orphans = 4
    ordering = "created_at"
    context_object_name = "posts"


class FAQPostDetailView(DetailView):

    """FAQPost Detail View Definition"""

    model = models.FAQPost
    context_object_name = "post"
