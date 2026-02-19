from rest_framework import viewsets, permissions
from .models import Metric, MetricRecord, Tag
from .serializers import (MetricSerializer, MetricRecordSerializer,
                          TagSerializer)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAdminUser]


class MetricViewSet(viewsets.ModelViewSet):
    serializer_class = MetricSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Metric.objects.all()

    def get_queryset(self):
        return Metric.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class MetricRecordViewSet(viewsets.ModelViewSet):
    serializer_class = MetricRecordSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Metric.objects.all()

    def get_queryset(self):
        user_metrics = Metric.objects.filter(user=self.request.user)
        return MetricRecord.objects.filter(metric__in=user_metrics)
