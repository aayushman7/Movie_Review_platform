from rest_framework import throttling

class ReviewListThrottling(throttling.UserRateThrottle):
    scope='review-list'


class ReviewCreateThrottling(throttling.UserRateThrottle):
    scope='review-create'