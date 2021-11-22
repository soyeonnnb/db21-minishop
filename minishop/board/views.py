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


def faq_detail(request, pk):
    post = models.FAQPost.objects.get(pk=pk)
    comments = models.FAQComment.objects.filter(post=post)
    return render(
        request, "board/faqpost_detail.html", {"post": post, "comments": comments}
    )
