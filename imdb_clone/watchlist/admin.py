from django.contrib import admin
from .models import Review, StreamPlatform, WatchList
# Register your models here.

admin.site.register(Review)
admin.site.register(StreamPlatform)
admin.site.register(WatchList)