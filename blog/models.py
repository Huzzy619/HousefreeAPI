from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
class Blog(models.Model):
	title = models.CharField(max_length=255)
	content = models.TextField()
	featured_image = models.ImageField(upload_to='blog_images')
	published_date = models.DateField()
	author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

	def __str__(self):
		return self.title

