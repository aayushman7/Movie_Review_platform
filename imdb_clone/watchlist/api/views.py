from rest_framework.viewsets import ViewSet
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.throttling import AnonRateThrottle,UserRateThrottle,ScopedRateThrottle
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from .pagination import WatchListCPagination,WatchListLOPagination,WatchListPagination
from watchlist.api.serializers import ReviewSerializer,WatchListSerializer,StreamPlatformSerializer
from watchlist.models import Review,WatchList,StreamPlatform
from watchlist.api.throttles import ReviewCreateThrottling,ReviewListThrottling
from watchlist.api.permissions import ReviewCreaterOrReadOnly,AdminOrReadOnly
# Create your views here.

class UserReviews(generics.ListAPIView):
    serializer_class=ReviewSerializer
    def get_queryset(self):
        username=self.request.query_params.get('username')
        reviews=Review.objects.filter(reviewer__username=username)

class ReviewList(generics.ListAPIView):
    serializer_class=ReviewSerializer
    throttle_classes=[AnonRateThrottle,ReviewListThrottling]
    filter_backends=[DjangoFilterBackend]

    def get_queryset(self):
        pk=self.kwargs['pk']
        return Review.objects.filter(watchlist=pk)

class ReviewCreate(generics.CreateAPIView):
    serializer_class=ReviewSerializer
    permission_classes=[IsAuthenticated]
    throttle_classes=[ReviewCreateThrottling]
    def get_queryset(self):
        return Review.objects.all
    
    def perform_create(self, serializer):
        pk=self.kwargs.get('pk')
        watchlist=WatchList.objects.get(pk=pk)

        reviewer=self.request.user
        queryset=Review.objects.filter(watchlist=watchlist,reviewer=reviewer).exists()
        
        if queryset:
            raise ValidationError("You have already reviewed")
        
        serializer.save(watchlist=watchlist,reviewer=reviewer)


class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset=Review.objects.all()
    serializer_class=ReviewSerializer
    permission_classes=[ReviewCreaterOrReadOnly]
    throttle_classes=[ScopedRateThrottle,AnonRateThrottle]
    throttle_scope='review-detail'

class StreamPlatformVS(viewsets.ModelViewSet):
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer
    permission_classes = [AdminOrReadOnly]
    throttle_classes = [AnonRateThrottle]


class WatchListGV(generics.ListAPIView):
    queryset = WatchList.objects.all()
    serializer_class = WatchListSerializer
    pagination_class = WatchListCPagination



class WatchListAV(APIView):
    permission_classes = [AdminOrReadOnly]
    throttle_classes = [AnonRateThrottle]

    def get(self, request):
        movies = WatchList.objects.all()
        serializer = WatchListSerializer(movies, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = WatchListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class WatchDetailAV(APIView):
    permission_classes = [AdminOrReadOnly]
    throttle_classes = [AnonRateThrottle]

    def get(self, request, pk):
        try:
            movie = WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = WatchListSerializer(movie)
        return Response(serializer.data)

    def put(self, request, pk):
        movie = WatchList.objects.get(pk=pk)
        serializer = WatchListSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        movie = WatchList.objects.get(pk=pk)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
