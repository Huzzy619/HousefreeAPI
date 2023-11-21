from django.contrib.auth import get_user_model
from django.db import models

from utils.paths.path_helpers import get_blogs_image_path


class Blog(models.Model):
    CATEGORY = [
        ("Spotlight", "Spotlight"),
        ("Buying & Selling", "Buying & Selling"),
        ("Renting", "Renting"),
        ("Tips & Advice", "Tips & Advice"),
    ]
    title = models.CharField(max_length=500)
    content = models.TextField()
    category = models.CharField(max_length=200, choices=CATEGORY)
    featured = models.BooleanField(default=False)
    image = models.ImageField(upload_to=get_blogs_image_path, null=True, blank=True)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    date_published = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-date_published"]
        verbose_name = "Post"

    def __str__(self):
        return self.title

    @property
    def author_name(self):
        return self.author.get_full_name()
