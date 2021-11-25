from django.utils import timezone
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from . import models
from . import forms
from users import mixins as users_mixins

# Create your views here.
class FAQListView(ListView):

    """FAQListView Definition"""

    model = models.FAQPost
    paginate_by = 15
    paginate_orphans = 4
    ordering = "-created_at"
    context_object_name = "posts"


def faq_post_detail(request, pk):
    post = models.FAQPost.objects.get(pk=pk)
    comments = models.FAQComment.objects.filter(post=post)
    comment_form = forms.CreateFAQCommentForm()

    return render(
        request,
        "board/faqpost_detail.html",
        {"post": post, "comments": comments, "comment_form": comment_form},
    )


def faqcomment_create(request, pk):
    filled_form = forms.CreateFAQCommentForm(request.POST)
    if filled_form.is_valid():
        finished_form = filled_form.save(commit=False)
        finished_form.post = get_object_or_404(models.FAQPost, pk=pk)
        finished_form.user = request.user
        finished_form.created_at = timezone.now()
        finished_form.updated_at = timezone.now()
        finished_form.save()
    return redirect("board:detail", pk)


@login_required
def faq_post_create(request):
    if request.method == "POST" or request.method == "FILES":
        form = forms.CreateFAQPostForm(request.POST, request.FILES)
        if form.is_valid():
            finished_form = form.save(commit=False)
            finished_form.user = request.user
            finished_form.save()
            request.FILES["imagename"].name
            return redirect(
                "board:detail",
                finished_form.pk,
            )

    else:
        form = forms.CreateFAQPostForm()

    return render(request, "board/faqpost_create.html", {"form": form})


def my_faqpost_view(request):
    user = request.user
    post_list = models.FAQPost.objects.filter(user=user).order_by("-created_at")
    paginator = Paginator(post_list, 15)
    page_num = request.GET.get("page")
    post_list = paginator.get_page(page_num)
    return render(request, "board/my_faqpost.html", {"post_list": post_list})


@method_decorator(login_required, name="dispatch")
class UpdatePostView(UpdateView):

    model = models.FAQPost
    template_name = "board/faqpost_update.html"
    fields = (
        "title",
        "body",
        "photo",
    )
    success_message = "게시물이 수정되었습니다"
    # 폼 입력방식 커스텀
    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields["title"].widget.attrs = {
            "placeholder": "제목",
            "class": "form-control",
            "id": "titleInput",
        }
        form.fields["body"].widget.attrs = {
            "class": "form-control",
            "id": "bodyInput",
            "aria-describedby": "bodyInput",
            "aria-label": "Body",
        }
        form.fields["photo"].widget.attrs = {
            "class": "form-control",
            "id": "photoInput",
        }
        return form

    def get_success_url(self):
        return reverse("board:my_faq")


class DeletePostView(users_mixins.LoggedInOnlyView, DeleteView):

    model = models.FAQPost
    context_object_name = "post"

    def get_success_url(self):
        return reverse_lazy("board:my_faq")

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
