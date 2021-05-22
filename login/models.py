from django.db import models

from PIL import Image
# class User(models.Model):
#     id = models.AutoField(primary_key=True)
#     username = models.CharField(max_length=30)
#     email = models.EmailField(max_length=50)
#     phone = models.CharField(max_length=10)
#     password = models.CharField(max_length=32)
#
#     def __str__(self):
#         return f'{self.username},{self.email}'

from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)