from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.core.validators import FileExtensionValidator


class Video(models.Model):
    uploader = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    video_file = models.FileField(upload_to='uploads/video_files', validators=[FileExtensionValidator(allowed_extensions=['mp4'])])
    thumbnail = models.FileField(upload_to='uploads/thumbnails', validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg'])])
    date_post = models.DateTimeField(default=timezone.datetime.now())
    category = models.ForeignKey('Category', on_delete=models.CASCADE)

    def __str__(self):
        return self.uploader_id


class Category(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey('Video', on_delete=models.CASCADE)
    comment = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Auhor: {self.author} | Created on: {self.created_on.strftime("%b %d %Y %I:%M %p")}'