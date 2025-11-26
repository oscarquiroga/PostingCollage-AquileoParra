from django.db import models
from django.conf import settings
from django_ckeditor_5.fields import CKEditor5Field

User = settings.AUTH_USER_MODEL

class Post(models.Model):
    STATUS_CHOICES = (
        ("pending", "Pending Review"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    title = models.CharField(max_length=255)
    body = CKEditor5Field(config_name="default")
    imgs = models.ImageField(upload_to="posts/images/", null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    feedback = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    views = models.IntegerField(default=0)
    tags = models.CharField(max_length=255, blank=True, help_text="Separar con comas (ej: deportes, ciencia, colegio)")

    links = models.TextField(null=True, blank=True, help_text="Ingresa enlaces separados por una nueva línea")

    attachment = models.FileField(upload_to="posts/files/", null=True, blank=True)

    video_url = models.URLField(null=True, blank=True)
    def __str__(self):
        return f"{self.title} - {self.user.username}"


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="liked_posts")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("post", "user")

    def __str__(self):
        return f"{self.user.username} liked {self.post.title}"
