from django.db import models

# Create your models here.
class FAQPost(models.Model):

    """FAQ Post Model Definition"""

    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    photo = models.ImageField(blank=True, null=True, upload_to="faq_photo")

    def __str__(self):
        return self.title


class FAQComment(models.Model):

    """FAQ Comment Definition"""

    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    post = models.ForeignKey(FAQPost, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
