from django.contrib import admin
from .models import Metric, MetricRecord, Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']


@admin.register(Metric)
class MetricAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'created_at']
    list_filter = ['user', 'created_at']
    search_fields = ['name', 'description']


@admin.register(MetricRecord)
class MetricRecordAdmin(admin.ModelAdmin):
    list_display = ['metric', 'value', 'timestamp', 'created_at']
    list_filter = ['metric__user', 'timestamp']
    date_hierarchy = 'timestamp'
