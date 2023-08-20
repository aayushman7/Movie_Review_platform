from django.urls import path,include

from watchlist.api import views
from rest_framework.routers import DefaultRouter
from watchlist.api.views import StreamPlatformVS

router=DefaultRouter()
router.register('platform',StreamPlatformVS,basename="stream-platform")

urlpatterns=[
    path('<int:pk>/review-create',views.ReviewCreate.as_view(),name="review-create"),
    path('<int:pk>/reviews',views.ReviewList.as_view(),name="review-list"),
    path('review/<int:pk>',views.ReviewDetail.as_view(),name="review-detail"),
    path('',include(router.urls)),
    path('<int:pk>/',views.WatchDetailAV.as_view(),name="watchlist-details"),
    path('list/',views.WatchListAV.as_view(),name="watch-list"),
    path('user_reviews/',views.UserReviews.as_view(),name="user-reviews"),
]
