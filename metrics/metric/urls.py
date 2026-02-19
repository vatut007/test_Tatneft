from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'tags', views.TagViewSet)
router.register(r'metrics', views.MetricViewSet, basename='metric')
router.register(r'records', views.MetricRecordViewSet, basename='metricRecord')

urlpatterns = [
    path('api/', include(router.urls)),
]
