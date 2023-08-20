from rest_framework import serializers

from watchlist.models import Review,StreamPlatform,WatchList


class ReviewSerializer(serializers.ModelSerializer):
    reviewer = serializers.StringRelatedField(read_only=True)
    watchlist=serializers.CharField(source='watchlist.name',read_only=True)
    class Meta:
        model=Review
        fields="__all__"

class WatchListSerializer(serializers.ModelSerializer):
    reviews=ReviewSerializer(many=True,read_only=True)
    # stream=serializers.CharField(queryset=StreamPlatform.objects.all(),source='stream.name')/
    class Meta:
        model=WatchList
        fields="__all__"

class StreamPlatformSerializer(serializers.ModelSerializer):
    watchlist=WatchListSerializer(many=True,read_only=True)
    class Meta:
        model=StreamPlatform
        fields="__all__"


