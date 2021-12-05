from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import ListView, UpdateView, DeleteView

from . import models
from . import forms
from users import mixins as users_mixins

# FAQ List를 보여주는 클래스
class FAQListView(ListView):

    """FAQListView Definition"""

    model = models.FAQPost
    paginate_by = 15  # 한 페이지에 15개씩 보여줌
    paginate_orphans = 4
    ordering = "-created_at"  # 최근에 생성된 글 순으로 정렬
    context_object_name = "posts"


# FAQ POST 내용을 보여주는 함수
def faq_post_detail(request, pk):
    post = models.FAQPost.objects.get(pk=pk)
    comments = models.FAQComment.objects.filter(post=post)
    comment_form = (
        forms.CreateFAQCommentForm()
    )  # 해당 페이지에서 comment form 도 있어야 하기 때문에 함께 가져옴
    return render(
        request,
        "board/faqpost_detail.html",
        {"post": post, "comments": comments, "comment_form": comment_form},
    )


# FAQ Detail Page에서 comment를 입력하였을 때 DB에 저장해주는 함수
@staff_member_required  # 유저 모델에서 is_staff가 true 인 유저만 작성 가능
def faqcomment_create(request, pk):
    filled_form = forms.CreateFAQCommentForm(request.POST)  # request가 POST형식이라면
    if filled_form.is_valid():
        finished_form = filled_form.save(commit=False)
        finished_form.post = get_object_or_404(models.FAQPost, pk=pk)  # POST를 가져옴
        finished_form.user = request.user  # 답변을 적은 사람을 요청을 보낸 사람으로 함
        finished_form.created_at = timezone.now()  # 날짜 저장
        finished_form.updated_at = timezone.now()  # 날짜 저장
        finished_form.save()  # DB에 저장함
    return redirect("board:detail", pk)


# 게시물 작성 함수
@login_required
def faq_post_create(request):
    if (
        request.method == "POST" or request.method == "FILES"
    ):  # 요청이 POST형식이라면, 해당 모델에는 사진도 있기 때문에 파일도 함께 가져옴
        form = forms.CreateFAQPostForm(request.POST, request.FILES)  #
        if form.is_valid():
            finished_form = form.save(commit=False)
            finished_form.user = request.user  # user 애트리뷰트는 요청을 보낸 user의 pk를 넣음
            finished_form.save()
            return redirect(
                "board:detail",
                finished_form.pk,
            )

    else:
        form = forms.CreateFAQPostForm()
    return render(request, "board/faqpost_create.html", {"form": form})


# 내가 작성한 post를 가져오는 함수
@login_required
def my_faqpost_view(request):
    user = request.user  # user는 요청을 보낸 유저임
    post_list = models.FAQPost.objects.filter(user=user).order_by(
        "-created_at"
    )  # FAQPost 모델에서 user가 요청을 보낸 유저인 post만 가져옴. 생성날짜가 빠른 순으로 정렬
    paginator = Paginator(post_list, 15)
    page_num = request.GET.get("page")
    post_list = paginator.get_page(page_num)
    return render(request, "board/my_faqpost.html", {"post_list": post_list})


# 게시물을 수정하는 클래스
@login_required
def faq_post_update(request, pk):
    faqpost = models.FAQPost.objects.get(pk=pk)  # 수정할 post 개체 가져오기
    if request.method == "POST" or request.method == "FILES":
        form = forms.UpdateFAQPostForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            body = form.cleaned_data["body"]
            photo = form.cleaned_data["photo"]
            faqpost.title = title  # 폼 저장
            faqpost.body = body
            faqpost.photo = photo
            faqpost.save()
            messages.success(request, "게시물이 수정되었습니다.")  # 완료 메세지 띄우기
        return redirect(reverse_lazy("board:my_faq"))

    else:
        form = forms.UpdateFAQPostForm(instance=faqpost)  # 수정할 개체 + 폼 가져오기
        return render(
            request,
            "board/faqpost_update.html",
            {"form": form},
        )


# 게시물을 삭제해주는 class
class DeletePostView(users_mixins.LoggedInOnlyView, DeleteView):

    model = models.FAQPost
    context_object_name = "post"

    def get_success_url(self):
        return reverse_lazy("board:my_faq")

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
