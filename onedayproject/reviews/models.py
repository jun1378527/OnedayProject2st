from django.db import models
from django.contrib.auth.models import User

class CodeReview(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField(default='')
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # nullable 제거
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    review = models.ForeignKey(CodeReview, related_name='comments', on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[:20]
