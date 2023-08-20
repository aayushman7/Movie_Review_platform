from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator,MaxValueValidator
# Create your models here.
class StreamPlatform(models.Model):
    name=models.CharField(max_length=50)
    website=models.URLField(max_length=100)

    def __str__(self) -> str:
        return self.name

class WatchList(models.Model):
    name=models.CharField(max_length=50)
    stream=models.ForeignKey(StreamPlatform,on_delete=models.CASCADE,related_name="watchlist")
    is_active=models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.name

class Review(models.Model):
    reviewer=models.ForeignKey(User,on_delete=models.CASCADE)
    rating=models.PositiveIntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    description=models.CharField(max_length=200,null=True,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    watchlist=models.ForeignKey(WatchList,on_delete=models.CASCADE,related_name="reviews")

    def __str__(self):
        return str(self.reviewer) +" "+ str(self.watchlist) +" "+ str(self.rating)