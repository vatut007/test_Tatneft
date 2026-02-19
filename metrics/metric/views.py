from http import HTTPStatus
from rest_framework import viewsets, permissions
from .models import Metric, MetricRecord, Tag
from .serializers import (MetricSerializer, MetricRecordSerializer,
                          TagSerializer)
from rest_framework.decorators import action
from rest_framework.response import Response
from django.core.cache import cache


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticated]


class MetricViewSet(viewsets.ModelViewSet):
    serializer_class = MetricSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Metric.objects.all()

    def get_queryset(self):
        return Metric.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['get', 'post'], url_path='records')
    def records(self, request, pk=None):
        """
        GET /api/metrics/{id}/records/ — список записей метрики (с кэшированием)
        POST /api/metrics/{id}/records/ — создание записи метрики
        """
        metric = self.get_object()

        if request.method == 'GET':
            cache_key = f'metric_{pk}_records_list'
            cached_data = cache.get(cache_key)

            if cached_data is not None:
                return Response(cached_data)

            records = metric.records.all()
            serializer = MetricRecordSerializer(records, many=True)
            data = serializer.data
            cache.set(cache_key, data, 300)  # кэш на 5 минут
            return Response(data)

        elif request.method == 'POST':
            serializer = MetricRecordSerializer(
                data=request.data,
                context={'metric': metric}
            )

            if serializer.is_valid():
                record = serializer.save()
                cache_key = f'metric_{pk}_records_list'
                cache.delete(cache_key)
                return Response(serializer.data,
                                status=HTTPStatus.CREATED)
            else:
                return Response(serializer.errors,
                                status=HTTPStatus.BAD_REQUEST)


class MetricRecordViewSet(viewsets.ModelViewSet):
    serializer_class = MetricRecordSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Metric.objects.all()

    def get_queryset(self):
        user_metrics = Metric.objects.filter(user=self.request.user)
        return MetricRecord.objects.filter(metric__in=user_metrics)
