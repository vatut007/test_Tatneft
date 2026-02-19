from rest_framework import serializers
from .models import Metric, MetricRecord, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'created_at']


class MetricSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Metric
        fields = ['id', 'user', 'name', 'description', 'created_at']


class MetricRecordSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    tag_ids = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        source='tags',
        many=True,
        write_only=True,
        required=False
    )

    class Meta:
        model = MetricRecord
        fields = ['id', 'metric', 'value', 'timestamp', 'tags', 'tag_ids',
                  'created_at']
