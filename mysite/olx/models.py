from django.db import models

# Create your models here.
class Seller(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()

class Post(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    image_url = models.CharField(max_length=128)
    pub_date = models.DateTimeField("date published")