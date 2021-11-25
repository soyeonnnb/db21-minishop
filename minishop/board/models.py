import os
from django.db import models

# Create your models here.


def faq_directory_path(instance, filename):
    return "faq_photo/post_{}/{}".format(instance.id, filename)


class FAQPost(models.Model):

    """FAQ Post Model Definition"""

    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    photo = models.ImageField(blank=True, null=True, upload_to=faq_directory_path)

    def __str__(self):
        return self.title

    def has_comments(self):
        all_comments = self.comments.all()
        return len(all_comments) > 0

    def save(self, *args, **kwargs):
        if self.id is None:
            temp_image = self.photo
            self.photo = None
            super().save(*args, **kwargs)
            self.photo = temp_image
            super().save(*args, **kwargs)


class FAQComment(models.Model):

    """FAQ Comment Definition"""

    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    post = models.ForeignKey(FAQPost, on_delete=models.CASCADE, related_name="comments")
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
