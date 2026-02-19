from pathlib import Path

from celery import shared_task
from .models import Metric
import os
from datetime import datetime


@shared_task
def create_fake_report() -> None:
    """
    Создаёт/обновляет текстовый файл с количеством записей в БД.
    """
    total_metrics = Metric.objects.count()
    report_dir = os.path.join(Path(__file__).parent.parent, 'reports')
    report_file = os.path.join(report_dir, 'fake_report.txt')
    content = (
        f"Отчёт от {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"Всего метрик: {total_metrics}\n"
    )
    try:
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Отчёт сохранён: {report_file}")
    except Exception as e:
        print(f"Ошибка при записи отчёта: {e}")
