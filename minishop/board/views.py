from django.shortcuts import render
from django.views.generic import ListView, CreateView
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

from . import models
from . import forms

# Create your views here.
class FAQListView(ListView):

    """FAQListView Definition"""

    model = models.FAQPost
    paginate_by = 12
    paginate_orphans = 4
    ordering = "created_at"
    context_object_name = "posts"


def faq_post_detail(request, pk):
    post = models.FAQPost.objects.get(pk=pk)
    comments = models.FAQComment.objects.filter(post=post)
    return render(
        request, "board/faqpost_detail.html", {"post": post, "comments": comments}
    )


@login_required
def faq_post_create(request):
    if request.method == "POST" or request.method == "FILES":
        form = forms.CreateFAQPostForm(request.POST, request.FILES)
        if form.is_valid():
            finished_form = form.save(commit=False)
            finished_form.user = request.user
            finished_form.save()
            return redirect(
                "board:detail",
                finished_form.pk,
            )

    else:
        form = forms.CreateFAQPostForm()

    return render(request, "board/faqpost_create.html", {"form": form})
