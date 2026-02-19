FROM python:3.12-slim
RUN pip install poetry==2.1.3
WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false
RUN poetry install --no-root
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
COPY /metrics .
ENTRYPOINT ["/entrypoint.sh"]
# CMD ["gunicorn", "metrics.wsgi:application", "--bind", "0.0.0.0:8000"]
